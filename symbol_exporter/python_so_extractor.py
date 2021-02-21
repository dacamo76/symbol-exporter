from enum import Enum
import argparse
from dataclasses import dataclass
import re
import struct
from typing import Optional
import logging
from pprint import pprint
from functools import lru_cache

import pwn

ASM_PATTERN = re.compile(r"^\s+([0-9a-f]+):\s+([0-9a-f]{2}(?: [0-9a-f]{2})*)(?:\s+([^\s]+)(?:\s+(.+?)\s*(?:# (0x[0-9a-f]+))?)?)?\s*$", re.MULTILINE)
PYMODULE_STRUCT = struct.Struct("x"*40 + "LLlL")
PYMETHOD_STRUCT = struct.Struct("LLixxxxL")

import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
	'%(log_color)s%(levelname)s:%(name)s:%(message)s'))
logger = logging.getLogger("pyso_extract")
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@dataclass
class AssemblyInstruction:
    loc_to_symbol: dict
    line: str
    data: str
    instruction: Optional[str]
    args: Optional[str]
    address: Optional[str]

    def __repr__(self):
        return "".join([
            self.line.rjust(8),
            ":       ",
            (self.data or "").ljust(24),
            (self.instruction or "").ljust(7),
            (self.args or "").ljust(30),
            (f"# [{self.symbol_name}]" if self.symbol_name else "").ljust(20),
        ])

    @property
    def symbol_name(self):
        return self.loc_to_symbol.get(self.address)


class Tracers(Enum):
    MODULE = "MODULE"
    SUBMODULE = "SUBMODULE"
    MODULE_DICT = "MODULE_DICT"



def initfunc_name(name):
    # See https://docs.python.org/3/extending/building.html#c.PyInit_modulename
    try:
        suffix = b'_' + name.encode('ascii')
    except UnicodeEncodeError:
        suffix = b'U_' + name.encode('punycode').replace(b'-', b'_')
    return 'PyInit' + suffix.decode("ascii")


def parse_create(elf, call: AssemblyInstruction, registers: dict, results: dict):
    module = registers["rdi"]

    module_struct_data = elf.read(int(module, base=16), PYMODULE_STRUCT.size)
    logger.debug("parse_module: module_struct_data is %s", list(map(hex, module_struct_data)))
    name, docs, size, methods_idx = PYMODULE_STRUCT.unpack(module_struct_data)
    assert name != 0, name
    name = elf.string(name).decode()
    if docs == 0:
        docs = None
    else:
        docs = elf.string(docs).decode()
    logger.debug("parse_module: Found module named %s", name)
    methods = []
    if methods_idx == 0:
        pass
        logger.debug("parse_module: No methods found, methods_idx is null")
    else:
        offset = 0
        while True:
            data = elf.read(methods_idx + offset, PYMETHOD_STRUCT.size)
            offset += PYMETHOD_STRUCT.size
            method_name, method_func, method_flags, method_doc = PYMETHOD_STRUCT.unpack(data)
            if method_name == 0:
                break
            method_name = elf.string(method_name).decode()
            if method_doc == 0:
                method_doc = None
            else:
                method_doc = elf.string(method_doc).decode()
            methods.append({"name": method_name, "docstring": method_doc})
            logger.info(
                "parse_create: Found %s in %s at %s",
                method_name, name, hex(method_func)
            )

    results["name"] = name
    results["docstring"] = docs
    results["methods"].extend(methods)

    registers["rax"] = Tracers.MODULE


def parse_new_submodule(elf, call: AssemblyInstruction, registers: dict, results: dict):
    if call.symbol_name == "PyModule_New":
        object_name = elf.string(int(registers["rdi"], 16)).decode()
    else:
        raise NotImplementedError(call.symbol_name)
    logger.info("parse_new_submodule: Found submodule %s", object_name)
    registers["rax"] = Tracers.SUBMODULE


def parse_add_object(elf, call: AssemblyInstruction, registers: dict, results: dict):
    if registers["rdi"] == Tracers.MODULE:
        object_name = elf.string(int(registers["rsi"], 16)).decode()
        results["objects"].append({"name": object_name})
        logger.info("parse_add_object: Found %s", object_name)
    else:
        logger.warning("Called parse_add_object with rdi=%s", registers["rdi"])


def PyModule_GetDict(elf, call: AssemblyInstruction, registers: dict, results: dict):
    if registers["rdi"] == Tracers.MODULE:
        registers["rax"] = Tracers.MODULE_DICT
    else:
        registers["rax"] = None


def PyDict_SetItemString(elf, call: AssemblyInstruction, registers: dict, results: dict):
    if registers["rdi"] == Tracers.MODULE_DICT:
        object_name = elf.string(int(registers["rsi"], 16)).decode()
        logger.info("Found call %s(module.__dict__, %s, %s)", call.symbol_name, object_name, registers["rdx"])
        results["objects"] += [{"name": object_name}]


KNOWN_SYMBOLS = {
    "PyModule_Create2": parse_create,
    "PyModuleDef_Init": parse_create,
    "PyModule_New": parse_new_submodule,
    "PyModule_NewObject": parse_new_submodule,
    "PyModule_AddObject": parse_add_object,
    "PyModule_AddIntConstant": parse_add_object,
    "PyModule_AddStringConstant": parse_add_object,
    "PyModule_GetDict": PyModule_GetDict,
    "PyDict_SetItemString": PyDict_SetItemString,
}


def parse_file(filename, module_name):
    elf = pwn.ELF(filename)

    # Find the locations of relaxant functions in the file
    loc_to_symbol = {}
    for symbol_name, symbol_loc in elf.symbols.items():
        if symbol_name.startswith(("got.", "plt.")):
            continue
        symbol_loc = hex(symbol_loc)
        logger.debug("Found symbol for %s at %s", symbol_name, symbol_loc)
        loc_to_symbol[symbol_loc] = symbol_name

    # Disassemble the PyInit function of the module
    results = {
        "methods": [],
        "objects": [],
    }
    emulate(elf, loc_to_symbol, initfunc_name(module_name), results)

    return results


disassembled_cache = {}

def disassemble_symbol(elf, loc_to_symbol: dict, function_name: str):
    global disassembled_cache
    if function_name not in disassembled_cache:
        init_asm = elf.functions[function_name].disasm()
        instructions = []
        logger.debug("Disassembled function (%s):", function_name)
        for line in init_asm.split("\n"):
            match = ASM_PATTERN.fullmatch(line)
            assert match, line
            instruction = AssemblyInstruction(loc_to_symbol, *match.groups())
            instructions.append(instruction)
            logger.debug(instruction)
        disassembled_cache[function_name] = instructions
    return disassembled_cache[function_name]


def emulate(elf, loc_to_symbol, function_name, results, registers=None):
    if registers is None:
        registers = {}
    instructions = disassemble_symbol(elf, loc_to_symbol, function_name)
    stack = []

    # Parse the assembly calling the parser functions in KNOWN_SYMBOLS when needed
    for instruction in instructions:
        logger.debug("Executing: %r", instruction)
        if instruction.instruction in ["lea"]:
            destination, source = map(str.strip, instruction.args.split(","))
            registers[destination] = instruction.address

        elif instruction.instruction in ["mov"]:
            destination, source = map(str.strip, instruction.args.split(","))
            
            if match := re.fullmatch(r"[DQ]WORD PTR \[([a-z0-9]{3})(\+0x0)?\]", destination):
                dest, offset = match.groups()
                destination = dest

            if instruction.address:
                registers[destination] = instruction.symbol_name
            else:
                registers[destination] = registers.get(source)

        elif instruction.instruction in ["push"]:
            source, = map(str.strip, instruction.args.split(","))
            stack += [registers.get(source)]

        elif instruction.instruction in ["pop"]:
            destination, = map(str.strip, instruction.args.split(","))
            if stack:
                registers[destination] = stack.pop()
            else:
                logger.warning("Tried to pop but the stack is empty!?")

        elif instruction.instruction in ["call", "jmp"]:
            if instruction.address:
                address = instruction.address
            else:
                address = instruction.args
            symbol_name = loc_to_symbol.get(address)
            logger.debug("Calling %s (%s) with register state:\n    %r", address, symbol_name, registers)
            if symbol_name in KNOWN_SYMBOLS:
                KNOWN_SYMBOLS[symbol_name](elf, instruction, registers, results)
            elif symbol_name in elf.functions:
                emulate(elf, loc_to_symbol, symbol_name, results, registers)
            else:
                logger.debug("Skipping call to %s (%s) as function definition is not available", address, symbol_name)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("module_name")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--compare")
    args = parser.parse_args()
    results = parse_file(args.filename, args.module_name)

    if args.print:
        pprint(results)

    if args.compare:
        import importlib
        module = importlib.import_module(args.compare)
        expected = {s for s in dir(module) if not re.fullmatch(r"__.+__", s)}
        actual = {x["name"] for x in results["methods"]}
        actual |= {x["name"] for x in results["objects"]}
        if actual - expected:
            raise NotImplementedError("Found unexpected keys", actual - expected)
        if expected - actual:
            logger.warning("Failed to find some keys: %s", expected - actual)


if __name__ == "__main__":
    parse_args()

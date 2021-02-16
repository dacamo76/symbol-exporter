import ast
import builtins
from typing import Any

# Increment when we need the database to be rebuilt (eg adding a new feature)
version = "0"
builtin_symbols = set(dir(builtins))


class SymbolFinder(ast.NodeVisitor):
    def __init__(self, module_name):
        self._module_name = module_name
        self.current_symbol_stack = [module_name]
        self.symbols = {
            module_name: {
                "type": "module",
                "data": {"lineno": None, "symbols_in_volume": set()},
            }
        }
        self.imported_symbols = []
        self.attr_stack = []
        self.used_symbols = set()
        self.aliases = {}
        self.undeclared_symbols = set()
        self.star_imports = set()
        self.used_builtins = set()

    def visit(self, node: ast.AST) -> Any:
        super().visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        self.imported_symbols.extend(k.name for k in node.names)
        for k in node.names:
            if not k.asname:
                self._add_import_to_surface_area(symbol=k.name, shadows=k.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module and node.level == 0:
            for k in node.names:
                if k.name != "*":
                    module_name = f"{node.module}.{k.name}"
                    self.aliases[k.name] = module_name
                    self.imported_symbols.append(module_name)
                    if not k.asname:
                        self._add_import_to_surface_area(
                            symbol=k.name, shadows=module_name
                        )
                else:
                    self.star_imports.add(node.module)
        self.generic_visit(node)

    def visit_alias(self, node: ast.alias) -> Any:
        if node.asname:
            alias_name = self.aliases.get(node.name, node.name)
            self.aliases[node.asname] = alias_name
            self._add_import_to_surface_area(symbol=node.asname, shadows=alias_name)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        self.attr_stack.append(node.attr)
        self.generic_visit(node)
        self.attr_stack.pop(-1)

    def visit_Assign(self, node: ast.Assign) -> Any:
        # TODO: handle multiple assignments
        # TODO: handle inside class
        # TODO: handle self?
        if len(node.targets) == 1 and len(self.current_symbol_stack) == 1:
            for target in node.targets:
                if hasattr(target, "id"):
                    self.current_symbol_stack.append(target.id)
                    self.symbols[self._symbol_stack_to_symbol_name()] = dict(
                        type="constant",
                        data={"lineno": node.lineno, "symbols_in_volume": set()},
                    )
            self.generic_visit(node)
            self.current_symbol_stack.pop(-1)
        else:
            self.generic_visit(node)

    def _symbol_stack_to_symbol_name(self):
        return ".".join(self.current_symbol_stack)

    def visit_Call(self, node: ast.Call) -> Any:
        if (
            hasattr(node.func, "id")
            and node.func.id not in self.aliases
            and node.func.id not in builtin_symbols
            and not self._symbol_in_surface_area(node.func.id)
        ):
            self.undeclared_symbols.add(node.func.id)
        tmp_stack = self.attr_stack.copy()
        self.attr_stack.clear()
        self.generic_visit(node)
        self.attr_stack = tmp_stack

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.current_symbol_stack.append(node.name)
        self.symbols[self._symbol_stack_to_symbol_name()] = dict(
            type="function", data={"lineno": node.lineno, "symbols_in_volume": set()}
        )
        self.generic_visit(node)
        self.current_symbol_stack.pop(-1)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.current_symbol_stack.append(node.name)
        self.symbols[self._symbol_stack_to_symbol_name()] = dict(
            type="class", data={"lineno": node.lineno, "symbols_in_volume": set()}
        )
        # self.aliases["self"] = node.name
        self.generic_visit(node)
        self.current_symbol_stack.pop(-1)
        # self.aliases.pop("self")

    def visit_Name(self, node: ast.Name) -> Any:
        def get_symbol_name(name):
            return self._symbol_in_surface_area(name) or ".".join(
                [name] + list(reversed(self.attr_stack))
            )

        name = self.aliases.get(node.id, node.id)
        if name in builtin_symbols:
            self.used_builtins.add(name)
        if self._symbol_previously_seen(name):
            symbol_name = get_symbol_name(name)
            if not self._is_constant(symbol_name):
                self.used_symbols.add(symbol_name)
            # Do not add myself to my own volume.
            # A previously declared symbol in the module is being referenced.
            surface_symbol = self._symbol_stack_to_symbol_name()
            if symbol_name != surface_symbol:
                if self._is_constant(surface_symbol):
                    self.symbols[self._module_name]["data"]["symbols_in_volume"].add(
                        symbol_name
                    )
                else:
                    self.symbols[surface_symbol]["data"]["symbols_in_volume"].add(
                        symbol_name
                    )
        self.generic_visit(node)

    def _is_constant(self, symbol_name):
        return self.symbols.get(symbol_name, {}).get("type") == "constant"

    def _symbol_previously_seen(self, symbol):
        return (
            symbol in self.imported_symbols
            or symbol in self.undeclared_symbols
            or symbol in builtin_symbols
            or self._symbol_in_surface_area(symbol)
        )

    def _symbol_in_surface_area(self, symbol):
        fully_qualified_symbol_name = f"{self._module_name}.{symbol}"
        if fully_qualified_symbol_name in self.symbols:
            return fully_qualified_symbol_name
        else:
            return None

    def _add_import_to_surface_area(self, symbol, shadows):
        full_symbol_name = f"{self._module_name}.{symbol}"
        self.symbols[full_symbol_name] = dict(
            type="import", data={"lineno": None, "shadows": shadows}
        )


# 1. get all the imports and their aliases (which includes imported things)
# 2. walk the ast find all usages of those aliases and log all the names and attributes used
# 3. trim those down to symbols (not class attributes)

# TODO: need to handle multiple assignment aliasing
#  Track which data is in what symbols (eg. a symbol is used inside a function definition) so we can build the web
#  of dependencies
#  Just pull all the assignments, aliases, functions and classes and then we don't need jedi (maybe) this would cause
#  us to not handle star imports, which need to be handled specially since their results are version dependant

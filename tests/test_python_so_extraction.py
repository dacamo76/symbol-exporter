import pytest

from symbol_exporter import python_so_extractor


def compare(filename, module_name, expected):
    python_so_extractor.disassembled_cache = {}
    results = python_so_extractor.parse_file(filename, module_name)
    actual = {x["name"] for x in results["methods"]}
    actual |= {x["name"] for x in results["objects"]}
    diff = (actual - expected)
    assert not diff, (f"Found {len(diff)} extra keys", diff)
    diff = (expected - actual)
    assert not diff, (f"Failed to find {len(diff)} out of {len(expected)} keys", diff)


def test__sha1():
    expected = {'SHA1Type', 'sha1'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_sha1.cpython-37m-x86_64-linux-gnu.so", "_sha1", expected)


def test__sha256():
    expected = {'SHA224Type', 'SHA256Type', 'sha224', 'sha256'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_sha256.cpython-37m-x86_64-linux-gnu.so", "_sha256", expected)


def test__sha3():
    expected = {'implementation', 'keccakopt', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128', 'shake_256'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_sha3.cpython-37m-x86_64-linux-gnu.so", "_sha3", expected)


def test__sha512():
    expected = {'SHA384Type', 'SHA512Type', 'sha384', 'sha512'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_sha512.cpython-37m-x86_64-linux-gnu.so", "_sha512", expected)


def test_zlib():
    expected = {'DEFLATED', 'DEF_BUF_SIZE', 'DEF_MEM_LEVEL', 'MAX_WBITS', 'ZLIB_RUNTIME_VERSION', 'ZLIB_VERSION', 'Z_BEST_COMPRESSION', 'Z_BEST_SPEED', 'Z_BLOCK', 'Z_DEFAULT_COMPRESSION', 'Z_DEFAULT_STRATEGY', 'Z_FILTERED', 'Z_FINISH', 'Z_FIXED', 'Z_FULL_FLUSH', 'Z_HUFFMAN_ONLY', 'Z_NO_COMPRESSION', 'Z_NO_FLUSH', 'Z_PARTIAL_FLUSH', 'Z_RLE', 'Z_SYNC_FLUSH', 'Z_TREES', 'adler32', 'compress', 'compressobj', 'crc32', 'decompress', 'decompressobj', 'error', '__version__'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/zlib.cpython-37m-x86_64-linux-gnu.so", "zlib", expected)


def test_math():
    expected = {'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi', 'pow', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/math.cpython-37m-x86_64-linux-gnu.so", "math", expected)


def test_mmap():
    expected = {'ACCESS_COPY', 'ACCESS_DEFAULT', 'ACCESS_READ', 'ACCESS_WRITE', 'ALLOCATIONGRANULARITY', 'MAP_ANON', 'MAP_ANONYMOUS', 'MAP_DENYWRITE', 'MAP_EXECUTABLE', 'MAP_PRIVATE', 'MAP_SHARED', 'PAGESIZE', 'PROT_EXEC', 'PROT_READ', 'PROT_WRITE', 'error', 'mmap'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/mmap.cpython-37m-x86_64-linux-gnu.so", "mmap", expected)


def test__md5():
    expected = {'MD5Type', 'md5'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_md5.cpython-37m-x86_64-linux-gnu.so", "_md5", expected)


def test__json():
    expected = {'encode_basestring', 'encode_basestring_ascii', 'make_encoder', 'make_scanner', 'scanstring'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_json.cpython-37m-x86_64-linux-gnu.so", "_json", expected)


def test__bz2():
    expected = {'BZ2Compressor', 'BZ2Decompressor'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/_bz2.cpython-37m-x86_64-linux-gnu.so", "_bz2", expected)


@pytest.mark.xfail(strict=True)
def test__curses_py37():
    expected = {'KEY_BREAK', 'KEY_F42', 'def_prog_mode', 'KEY_SCANCEL', 'KEY_RESIZE', 'KEY_SCOMMAND', 'KEY_SEND', 'KEY_F21', 'KEY_MARK', 'KEY_SPRINT', 'KEY_SEXIT', 'KEY_SHELP', 'KEY_STAB', 'KEY_MESSAGE', 'KEY_F48', 'unctrl', 'KEY_F59', 'KEY_IL', 'has_ic', 'reset_shell_mode', 'is_term_resized', 'KEY_FIND', 'nonl', 'BUTTON3_RELEASED', 'A_LOW', 'KEY_CLEAR', 'KEY_F34', 'curs_set', 'KEY_PPAGE', 'KEY_F1', 'def_shell_mode', 'KEY_BACKSPACE', 'KEY_SRIGHT', 'BUTTON2_PRESSED', 'BUTTON_CTRL', 'killchar', 'BUTTON4_DOUBLE_CLICKED', 'COLOR_RED', 'KEY_HOME', 'KEY_F54', 'KEY_F49', 'KEY_F6', 'delay_output', 'A_BLINK', 'KEY_COPY', 'tigetstr', 'KEY_SRESET', 'can_change_color', 'endwin', 'filter', 'KEY_F58', 'version', 'KEY_F16', 'KEY_CTAB', 'tigetflag', 'A_VERTICAL', 'KEY_F30', 'KEY_F19', 'KEY_SR', 'KEY_END', 'A_STANDOUT', 'REPORT_MOUSE_POSITION', 'KEY_F3', 'KEY_F63', 'termattrs', 'A_ALTCHARSET', 'BUTTON3_TRIPLE_CLICKED', 'BUTTON2_DOUBLE_CLICKED', 'KEY_F41', 'longname', 'termname', 'KEY_F45', 'pair_content', 'pair_number', 'KEY_LL', 'KEY_IC', 'KEY_REPLACE', 'KEY_F10', 'error', 'A_TOP', 'meta', 'BUTTON2_CLICKED', 'KEY_F46', 'KEY_F7', 'BUTTON1_RELEASED', 'KEY_HELP', 'A_COLOR', 'KEY_F12', 'initscr', 'KEY_F17', 'KEY_C3', 'BUTTON1_DOUBLE_CLICKED', 'KEY_F20', 'KEY_F32', 'resetty', 'KEY_RESUME', 'KEY_RIGHT', 'A_PROTECT', 'KEY_LEFT', 'ungetmouse', 'KEY_F57', 'halfdelay', 'A_RIGHT', 'KEY_RESTART', 'BUTTON4_PRESSED', 'KEY_SOPTIONS', 'KEY_F29', 'KEY_SCOPY', 'BUTTON4_TRIPLE_CLICKED', 'doupdate', 'KEY_RESET', 'savetty', 'COLOR_BLACK', 'COLOR_WHITE', 'KEY_F55', 'KEY_SBEG', 'KEY_F0', 'BUTTON4_CLICKED', 'KEY_F28', 'KEY_SNEXT', 'resize_term', 'mousemask', 'update_lines_cols', 'BUTTON_ALT', 'KEY_F2', 'KEY_F14', 'KEY_OPTIONS', 'KEY_SCREATE', 'noraw', 'A_ATTRIBUTES', 'KEY_F37', 'KEY_SUNDO', 'KEY_SREPLACE', 'KEY_CANCEL', 'BUTTON3_PRESSED', 'KEY_F36', 'KEY_SIC', 'setsyx', 'A_NORMAL', 'KEY_F60', 'BUTTON1_PRESSED', 'tparm', 'KEY_SAVE', 'KEY_ENTER', 'KEY_SPREVIOUS', 'KEY_EXIT', 'has_il', 'KEY_F62', 'noqiflush', 'KEY_DOWN', 'putp', 'keyname', 'ungetch', 'A_DIM', 'A_ITALIC', 'KEY_SLEFT', 'KEY_F51', 'KEY_F23', 'KEY_SMOVE', 'KEY_MOUSE', 'KEY_MOVE', 'A_BOLD', 'COLOR_MAGENTA', 'KEY_MAX', 'KEY_UP', 'KEY_SRSUME', 'KEY_F25', 'KEY_EOL', 'KEY_F33', 'KEY_EOS', 'intrflush', 'newpad', 'has_key', 'start_color', 'KEY_SFIND', 'KEY_SDC', 'BUTTON3_DOUBLE_CLICKED', 'A_INVIS', 'KEY_F26', 'KEY_F52', 'tigetnum', 'KEY_F44', 'KEY_CREATE', 'napms', 'nl', 'KEY_EIC', 'A_CHARTEXT', 'KEY_REDO', 'KEY_F11', 'A_UNDERLINE', 'KEY_SDL', 'resizeterm', 'color_pair', 'isendwin', 'COLOR_CYAN', 'baudrate', 'raw', 'setupterm', 'flash', 'KEY_F18', 'KEY_F50', 'BUTTON3_CLICKED', 'KEY_NEXT', 'KEY_DL', '_C_API', 'BUTTON2_TRIPLE_CLICKED', 'init_pair', 'COLOR_BLUE', 'init_color', 'newwin', 'KEY_CATAB', 'KEY_SELECT', 'KEY_F22', 'mouseinterval', 'reset_prog_mode', 'KEY_F13', 'KEY_SEOL', 'has_colors', 'unget_wch', 'getwin', 'erasechar', 'KEY_C1', 'noecho', 'getmouse', 'KEY_F24', 'BUTTON2_RELEASED', 'A_REVERSE', 'KEY_BEG', 'A_LEFT', 'BUTTON1_TRIPLE_CLICKED', 'KEY_F5', 'KEY_CLOSE', 'KEY_OPEN', 'KEY_A3', 'KEY_F8', 'KEY_REFRESH', 'typeahead', 'use_env', 'KEY_F27', 'KEY_F47', 'KEY_F56', 'BUTTON4_RELEASED', 'KEY_F61', 'KEY_A1', 'BUTTON1_CLICKED', 'KEY_F35', 'KEY_F53', 'OK', 'A_HORIZONTAL', 'KEY_SHOME', 'COLOR_YELLOW', 'KEY_REFERENCE', 'BUTTON_SHIFT', 'KEY_F38', 'cbreak', 'color_content', 'KEY_COMMAND', 'KEY_F15', 'KEY_DC', 'KEY_F43', 'beep', 'use_default_colors', 'KEY_SREDO', 'KEY_SSUSPEND', 'ALL_MOUSE_EVENTS', 'ERR', 'KEY_F31', 'KEY_F9', 'nocbreak', 'KEY_SSAVE', 'KEY_F40', 'KEY_F39', 'KEY_SUSPEND', 'KEY_BTAB', 'KEY_MIN', 'KEY_NPAGE', 'KEY_PREVIOUS', 'echo', 'COLOR_GREEN', 'KEY_B2', 'getsyx', 'KEY_SMESSAGE', 'KEY_PRINT', 'KEY_F4', 'KEY_UNDO', 'KEY_SF', 'flushinp', 'qiflush'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_curses.cpython-37m-x86_64-linux-gnu.so', '_curses', expected)


@pytest.mark.xfail(strict=True)
def test__csv_py37():
    expected = {'field_size_limit', '_dialects', 'get_dialect', 'reader', 'QUOTE_ALL', 'QUOTE_NONNUMERIC', 'Dialect', 'QUOTE_MINIMAL', 'unregister_dialect', 'Error', 'register_dialect', 'QUOTE_NONE', 'writer', 'list_dialects'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_csv.cpython-37m-x86_64-linux-gnu.so', '_csv', expected)


def test_binascii():
    expected = {'Error', 'Incomplete', 'a2b_base64', 'a2b_hex', 'a2b_hqx', 'a2b_qp', 'a2b_uu', 'b2a_base64', 'b2a_hex', 'b2a_hqx', 'b2a_qp', 'b2a_uu', 'crc32', 'crc_hqx', 'hexlify', 'rlecode_hqx', 'rledecode_hqx', 'unhexlify'}
    compare("/home/cburr/miniconda3/lib/python3.7/lib-dynload/binascii.cpython-37m-x86_64-linux-gnu.so", "binascii", expected)


@pytest.mark.xfail(strict=True)
def test_ctypes():
    expected = {'POINTER', 'Union', 'pointer', 'PyObj_FromPtr', 'FUNCFLAG_USE_ERRNO', 'Array', 'sizeof', '_memmove_addr', 'ArgumentError', 'RTLD_LOCAL', '_wstring_at_addr', '_string_at_addr', 'get_errno', '_pointer_type_cache', 'buffer_info', 'byref', 'addressof', '_cast_addr', 'Structure', 'dlclose', 'call_function', 'FUNCFLAG_PYTHONAPI', '_Pointer', 'FUNCFLAG_USE_LASTERROR', 'Py_INCREF', 'CFuncPtr', 'dlsym', 'FUNCFLAG_CDECL', '_memset_addr', 'Py_DECREF', '_SimpleCData', 'set_errno', 'RTLD_GLOBAL', 'call_cdeclfunction', 'dlopen', '_unpickle', 'alignment', 'resize'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_ctypes.cpython-37m-x86_64-linux-gnu.so', '_ctypes', expected)


def test_cmath():
    expected = {'cosh', 'tanh', 'atan', 'log', 'acosh', 'isclose', 'phase', 'cos', 'sin', 'inf', 'log10', 'acos', 'isfinite', 'nan', 'exp', 'polar', 'tan', 'nanj', 'sinh', 'atanh', 'e', 'sqrt', 'asin', 'rect', 'asinh', 'isnan', 'tau', 'pi', 'infj', 'isinf'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/cmath.cpython-37m-x86_64-linux-gnu.so', 'cmath', expected)


def test_blake2():
    expected = {'BLAKE2B_SALT_SIZE', 'BLAKE2S_SALT_SIZE', 'BLAKE2S_MAX_KEY_SIZE', 'BLAKE2S_MAX_DIGEST_SIZE', 'blake2s', 'BLAKE2S_PERSON_SIZE', 'BLAKE2B_PERSON_SIZE', 'blake2b', 'BLAKE2B_MAX_KEY_SIZE', 'BLAKE2B_MAX_DIGEST_SIZE'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_blake2.cpython-37m-x86_64-linux-gnu.so', '_blake2', expected)


def test_nis():
    expected = {'maps', 'get_default_domain', 'match', 'error', 'cat'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/nis.cpython-37m-x86_64-linux-gnu.so', 'nis', expected)


def test_parser():
    expected = {'__copyright__', '__doc__', '__version__', 'expr', 'STType', 'compilest', 'sequence2st', 'tuple2st', '_pickler', 'isexpr', 'suite', 'st2tuple', 'issuite', 'ParserError', 'st2list'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/parser.cpython-37m-x86_64-linux-gnu.so', 'parser', expected)


def test_pickle():
    expected = {'PickleError', 'Pickler', 'dump', 'UnpicklingError', 'PicklingError', 'loads', 'load', 'Unpickler', 'dumps'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_pickle.cpython-37m-x86_64-linux-gnu.so', '_pickle', expected)


def test_pyexpat():
    expected = {'XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE', 'XML_PARAM_ENTITY_PARSING_NEVER', 'error', 'ErrorString', 'XMLParserType', 'features', 'EXPAT_VERSION', 'errors', 'XML_PARAM_ENTITY_PARSING_ALWAYS', 'model', 'native_encoding', 'ParserCreate', 'expat_CAPI', 'ExpatError', 'version_info'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/pyexpat.cpython-37m-x86_64-linux-gnu.so', 'pyexpat', expected)


def test_random():
    expected = {'Random'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_random.cpython-37m-x86_64-linux-gnu.so', '_random', expected)


def test_select():
    expected = {'EPOLLIN', 'POLLWRBAND', 'EPOLLONESHOT', 'EPOLLMSG', 'EPOLLERR', 'EPOLLRDNORM', 'EPOLLOUT', 'POLLHUP', 'EPOLLWRNORM', 'POLLIN', 'POLLWRNORM', 'POLLRDBAND', 'PIPE_BUF', 'POLLNVAL', 'POLLRDNORM', 'POLLMSG', 'poll', 'EPOLLWRBAND', 'select', 'EPOLLHUP', 'EPOLLRDHUP', 'EPOLLRDBAND', 'epoll', 'EPOLLPRI', 'POLLOUT', 'POLLPRI', 'POLLERR', 'EPOLLET', 'POLLRDHUP', 'error', 'EPOLL_CLOEXEC'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/select.cpython-37m-x86_64-linux-gnu.so', 'select', expected)


def test_asyncio():
    expected = {'_enter_task', '_set_running_loop', 'get_event_loop', 'Task', '_register_task', '_all_tasks', 'Future', '_get_running_loop', '_leave_task', '_unregister_task', '_current_tasks', 'get_running_loop'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_asyncio.cpython-37m-x86_64-linux-gnu.so', '_asyncio', expected)


def test_bisect():
    expected = {'bisect_right', 'insort_left', 'insort_right', 'bisect_left'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_bisect.cpython-37m-x86_64-linux-gnu.so', '_bisect', expected)


@pytest.mark.xfail(strict=True)
def test_codecs_cn():
    expected = {'__map_gb2312', '__map_gb18030ext', '__map_gbcommon', 'getcodec', '__map_gbkext'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_cn.cpython-37m-x86_64-linux-gnu.so', '_codecs_cn', expected)


@pytest.mark.xfail(strict=True)
def test_codecs_hk():
    expected = {'__map_big5hkscs_nonbmp', '__map_big5hkscs_bmp', 'getcodec', '__map_big5hkscs'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_hk.cpython-37m-x86_64-linux-gnu.so', '_codecs_hk', expected)


def test_codecs_iso2022():
    expected = {'getcodec'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_iso2022.cpython-37m-x86_64-linux-gnu.so', '_codecs_iso2022', expected)


@pytest.mark.xfail(strict=True)
def test_codecs_jp():
    expected = {'__map_jisx0212', '__map_jisx0213_1_emp', '__map_jisx0208', '__map_jisx0213_emp', '__map_jisx0213_2_bmp', '__map_jisx0213_pair', 'getcodec', '__map_jisx0213_2_emp', '__map_cp932ext', '__map_jisxcommon', '__map_jisx0213_bmp', '__map_jisx0213_1_bmp'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_jp.cpython-37m-x86_64-linux-gnu.so', '_codecs_jp', expected)


@pytest.mark.xfail(strict=True)
def test_codecs_kr():
    expected = {'__map_ksx1001', '__map_cp949ext', '__map_cp949', 'getcodec'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_kr.cpython-37m-x86_64-linux-gnu.so', '_codecs_kr', expected)


@pytest.mark.xfail(strict=True)
def test_codecs_tw():
    expected = {'getcodec', '__map_cp950ext', '__map_big5'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_codecs_tw.cpython-37m-x86_64-linux-gnu.so', '_codecs_tw', expected)


def test_contextvars():
    expected = {'copy_context', 'ContextVar', 'Token', 'Context'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_contextvars.cpython-37m-x86_64-linux-gnu.so', '_contextvars', expected)


def test_crypt():
    expected = {'crypt'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_crypt.cpython-37m-x86_64-linux-gnu.so', '_crypt', expected)


def test_ctypes_test():
    expected = {'func', 'func_si'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_ctypes_test.cpython-37m-x86_64-linux-gnu.so', '_ctypes_test', expected)


@pytest.mark.xfail(strict=True)
def test_curses_panel():
    expected = {'new_panel', 'top_panel', 'error', 'version', 'update_panels', 'bottom_panel'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_curses_panel.cpython-37m-x86_64-linux-gnu.so', '_curses_panel', expected)


def test_datetime():
    expected = {'MINYEAR', 'timezone', 'MAXYEAR', 'timedelta', 'datetime', 'tzinfo', 'time', 'date', 'datetime_CAPI'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_datetime.cpython-37m-x86_64-linux-gnu.so', '_datetime', expected)


@pytest.mark.xfail(strict=True)
def test_decimal():
    expected = {'FloatOperation', 'MIN_EMIN', 'DivisionByZero', 'DecimalException', 'ConversionSyntax', 'MIN_ETINY', 'ROUND_CEILING', 'Decimal', 'ROUND_UP', 'Rounded', 'Underflow', 'HAVE_THREADS', 'Clamped', 'InvalidOperation', 'Subnormal', 'setcontext', 'MAX_PREC', 'localcontext', 'ROUND_DOWN', 'DivisionUndefined', 'ROUND_HALF_UP', 'DefaultContext', 'ROUND_HALF_DOWN', 'DivisionImpossible', 'Inexact', 'Context', 'DecimalTuple', 'Overflow', 'ROUND_05UP', 'InvalidContext', 'BasicContext', 'MAX_EMAX', 'getcontext', 'ExtendedContext', 'ROUND_FLOOR', 'ROUND_HALF_EVEN'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_decimal.cpython-37m-x86_64-linux-gnu.so', '_decimal', expected)


def test_elementtree():
    expected = {'TreeBuilder', 'XMLParser', 'SubElement', 'Element', 'ParseError'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_elementtree.cpython-37m-x86_64-linux-gnu.so', '_elementtree', expected)


def test_hashlib():
    expected = {'openssl_sha384', 'openssl_md5', 'openssl_sha512', 'pbkdf2_hmac', 'scrypt', 'openssl_sha224', 'hmac_digest', 'openssl_sha1', 'HASH', 'openssl_md_meth_names', 'new', 'openssl_sha256'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_hashlib.cpython-37m-x86_64-linux-gnu.so', '_hashlib', expected)


def test_heapq():
    expected = {'__about__', 'heapreplace', '_heapreplace_max', '_heapify_max', 'heappop', '_heappop_max', 'heappush', 'heapify', 'heappushpop'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_heapq.cpython-37m-x86_64-linux-gnu.so', '_heapq', expected)


def test_lsprof():
    expected = {'profiler_entry', 'Profiler', 'profiler_subentry'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_lsprof.cpython-37m-x86_64-linux-gnu.so', '_lsprof', expected)


def test_lzma():
    expected = {'CHECK_CRC32', 'MF_BT4', 'MODE_NORMAL', 'FILTER_SPARC', 'FORMAT_RAW', 'CHECK_ID_MAX', 'MODE_FAST', 'FILTER_ARM', 'FILTER_LZMA2', 'FILTER_DELTA', 'is_check_supported', 'MF_HC3', 'CHECK_SHA256', 'CHECK_CRC64', 'MF_BT3', 'PRESET_DEFAULT', 'LZMADecompressor', 'FORMAT_ALONE', 'FILTER_LZMA1', 'CHECK_NONE', 'PRESET_EXTREME', 'FILTER_ARMTHUMB', '_encode_filter_properties', 'FILTER_IA64', 'MF_BT2', '_decode_filter_properties', 'LZMAError', 'FILTER_X86', 'FILTER_POWERPC', 'MF_HC4', 'FORMAT_AUTO', 'LZMACompressor', 'CHECK_UNKNOWN', 'FORMAT_XZ'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_lzma.cpython-37m-x86_64-linux-gnu.so', '_lzma', expected)


@pytest.mark.xfail(strict=True)
def test_multibytecodec():
    expected = {'MultibyteStreamWriter', 'MultibyteIncrementalEncoder', 'MultibyteIncrementalDecoder', '__create_codec', 'MultibyteStreamReader'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_multibytecodec.cpython-37m-x86_64-linux-gnu.so', '_multibytecodec', expected)


def test_multiprocessing():
    expected = {'flags', 'sem_unlink', 'SemLock'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_multiprocessing.cpython-37m-x86_64-linux-gnu.so', '_multiprocessing', expected)


def test_opcode():
    expected = {'stack_effect'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_opcode.cpython-37m-x86_64-linux-gnu.so', '_opcode', expected)


def test_posixsubprocess():
    expected = {'fork_exec'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_posixsubprocess.cpython-37m-x86_64-linux-gnu.so', '_posixsubprocess', expected)


def test_queue():
    expected = {'Empty', 'SimpleQueue'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_queue.cpython-37m-x86_64-linux-gnu.so', '_queue', expected)


def test_socket():
    expected = {'SOCK_STREAM', 'CAN_RAW_FILTER', 'TIPC_WAIT_FOREVER', 'AF_DECnet', 'IPV6_RTHDR', 'MSG_EOR', 'IP_MAX_MEMBERSHIPS', 'EAI_NONAME', 'IPPROTO_SCTP', 'PACKET_OUTGOING', 'SO_SNDLOWAT', 'TIPC_HIGH_IMPORTANCE', 'IP_RECVOPTS', 'AI_ADDRCONFIG', 'CAN_RTR_FLAG', 'IPPROTO_DSTOPTS', 'getdefaulttimeout', 'INADDR_BROADCAST', 'PF_RDS', 'EAI_SOCKTYPE', 'setdefaulttimeout', 'SO_KEEPALIVE', 'INADDR_ANY', 'inet_pton', 'CAN_RAW_RECV_OWN_MSGS', 'IPV6_RECVHOPLIMIT', 'IP_MULTICAST_IF', 'if_indextoname', 'AF_UNSPEC', 'IP_DEFAULT_MULTICAST_LOOP', 'IPV6_MULTICAST_IF', 'AF_TIPC', 'CAN_ERR_MASK', 'IPV6_TCLASS', 'AI_NUMERICHOST', 'CMSG_SPACE', 'AI_PASSIVE', 'IPPROTO_TP', 'SOCK_DGRAM', 'AF_IRDA', 'IPPROTO_EGP', 'NI_MAXHOST', 'SOL_CAN_BASE', 'MSG_OOB', 'TCP_NODELAY', 'gethostbyname', 'IPPORT_RESERVED', 'SO_PASSCRED', 'if_nameindex', 'SOL_TIPC', 'IP_RECVRETOPTS', 'socket', 'AF_AX25', 'AF_RDS', 'IP_DROP_MEMBERSHIP', 'PF_CAN', 'AF_INET6', 'IPPROTO_RSVP', 'NETLINK_IP6_FW', 'IPV6_PKTINFO', 'SOCK_RAW', 'SocketType', 'MSG_NOSIGNAL', 'IPPROTO_ICMPV6', 'TIPC_IMPORTANCE', 'if_nametoindex', 'gethostbyaddr', 'ntohs', 'SO_PRIORITY', 'IPV6_RECVTCLASS', 'NETLINK_ROUTE', 'AF_ATMPVC', 'IPPROTO_HOPOPTS', 'SO_BROADCAST', 'AF_PACKET', 'ntohl', 'MSG_CMSG_CLOEXEC', 'has_ipv6', 'NETLINK_NFLOG', 'IP_MULTICAST_LOOP', 'EAI_MEMORY', 'EAI_ADDRFAMILY', 'SOCK_NONBLOCK', 'TIPC_ADDR_ID', 'TCP_CORK', 'IPPORT_USERRESERVED', 'htons', 'CAN_EFF_FLAG', 'NETLINK_XFRM', 'NI_MAXSERV', 'IPPROTO_UDP', 'AF_X25', 'CAN_ISOTP', 'SO_SNDTIMEO', 'SO_DOMAIN', 'SO_PEERSEC', 'SO_PROTOCOL', 'TCP_KEEPIDLE', 'getprotobyname', 'SOCK_SEQPACKET', 'IPV6_LEAVE_GROUP', 'PACKET_LOOPBACK', 'herror', 'IPPROTO_FRAGMENT', 'TIPC_SRC_DROPPABLE', 'NI_NOFQDN', 'SOL_SOCKET', 'AF_ASH', 'AF_PPPOX', 'IPV6_V6ONLY', 'IPPROTO_GRE', 'IP_DEFAULT_MULTICAST_TTL', 'PACKET_HOST', 'TIPC_CFG_SRV', 'INADDR_LOOPBACK', 'IPV6_MULTICAST_HOPS', 'MSG_ERRQUEUE', 'TIPC_CONN_TIMEOUT', 'TIPC_DEST_DROPPABLE', 'IPV6_DSTOPTS', 'PACKET_BROADCAST', 'TIPC_TOP_SRV', 'IPPROTO_IPIP', 'getaddrinfo', 'CMSG_LEN', 'SOL_TCP', 'TCP_WINDOW_CLAMP', 'SO_BINDTODEVICE', 'NI_NUMERICSERV', 'EAI_FAIL', 'SO_OOBINLINE', 'MSG_CTRUNC', 'AF_KEY', 'AI_CANONNAME', 'SO_ERROR', 'IPV6_RECVDSTOPTS', 'SOCK_CLOEXEC', 'IP_HDRINCL', 'EAI_BADFLAGS', 'AF_LLC', 'IP_TOS', 'SOL_UDP', 'EAI_FAMILY', 'SOL_CAN_RAW', 'TCP_KEEPINTVL', 'TCP_CONGESTION', 'AF_NETROM', 'getservbyname', 'IPPROTO_NONE', 'IPPROTO_ESP', 'AF_APPLETALK', 'NETLINK_FIREWALL', 'IPV6_CHECKSUM', 'sethostname', 'SHUT_RDWR', 'AF_ROSE', 'EAI_SYSTEM', 'CAN_RAW_ERR_FILTER', 'SO_REUSEADDR', 'NI_DGRAM', 'inet_aton', 'CAPI', 'inet_ntop', 'AF_NETBEUI', 'TCP_QUICKACK', 'AF_BRIDGE', 'SHUT_WR', 'IP_ADD_MEMBERSHIP', 'IPPROTO_RAW', 'IPV6_RTHDR_TYPE_0', 'inet_ntoa', 'TIPC_SUB_PORTS', 'IP_RETOPTS', 'CAN_EFF_MASK', 'IPPROTO_PUP', 'IPPROTO_PIM', 'SO_DONTROUTE', 'socketpair', 'TIPC_SUBSCR_TIMEOUT', 'AI_ALL', 'IP_MULTICAST_TTL', 'getnameinfo', 'EAI_NODATA', 'SO_PASSSEC', 'IPV6_MULTICAST_LOOP', 'MSG_WAITALL', 'TCP_INFO', 'CAN_RAW_LOOPBACK', 'SO_RCVLOWAT', 'htonl', 'EAI_SERVICE', 'MSG_PEEK', 'SHUT_RD', 'IPPROTO_ICMP', 'SO_LINGER', 'TCP_LINGER2', 'AF_SNA', 'gaierror', 'TIPC_MEDIUM_IMPORTANCE', 'SCM_RIGHTS', 'AF_ATMSVC', 'EAI_OVERFLOW', 'PACKET_OTHERHOST', 'SO_MARK', 'TIPC_SUB_SERVICE', 'PF_PACKET', 'MSG_DONTROUTE', 'TIPC_CRITICAL_IMPORTANCE', 'AF_ECONET', 'IPV6_RTHDRDSTOPTS', 'TIPC_LOW_IMPORTANCE', 'AF_ROUTE', 'dup', 'gethostname', 'CAN_SFF_MASK', 'TCP_DEFER_ACCEPT', 'TCP_SYNCNT', 'NI_NAMEREQD', 'IPPROTO_AH', 'AI_V4MAPPED', 'IPV6_HOPLIMIT', 'SO_ACCEPTCONN', 'TCP_MAXSEG', 'IPV6_NEXTHOP', 'timeout', 'error', 'SO_DEBUG', 'TIPC_CLUSTER_SCOPE', 'AF_IPX', 'TCP_KEEPCNT', 'IPPROTO_IDP', 'IPV6_HOPOPTS', 'IPPROTO_IGMP', 'IPPROTO_TCP', 'IPV6_RECVPKTINFO', 'AF_SECURITY', 'MSG_CONFIRM', 'SO_PEERCRED', 'INADDR_UNSPEC_GROUP', 'SCM_CREDENTIALS', 'SO_TYPE', 'TIPC_SUB_CANCEL', 'AF_INET', 'IPV6_JOIN_GROUP', 'CAN_RAW', 'IPV6_UNICAST_HOPS', 'IPPROTO_ROUTING', 'AF_UNIX', 'INADDR_NONE', 'INADDR_MAX_LOCAL_GROUP', 'SO_SNDBUF', 'SO_RCVBUF', 'TIPC_ADDR_NAMESEQ', 'NETLINK_USERSOCK', 'TIPC_ZONE_SCOPE', 'IP_TRANSPARENT', 'IP_TTL', 'PACKET_FASTROUTE', 'AI_NUMERICSERV', 'IPV6_RECVRTHDR', 'TIPC_PUBLISHED', 'AF_WANPIPE', 'IP_OPTIONS', 'CAN_ERR_FLAG', 'AF_CAN', 'MSG_TRUNC', 'TIPC_WITHDRAWN', 'close', 'AF_NETLINK', 'IPPROTO_IP', 'IPV6_RECVHOPOPTS', 'NI_NUMERICHOST', 'NETLINK_DNRTMSG', 'PACKET_MULTICAST', 'MSG_MORE', 'IPPROTO_IPV6', 'MSG_DONTWAIT', 'SOL_IP', 'SO_RCVTIMEO', 'INADDR_ALLHOSTS_GROUP', 'SOCK_RDM', 'TIPC_ADDR_NAME', 'EAI_AGAIN', 'TIPC_NODE_SCOPE', 'getservbyport', 'SOMAXCONN', 'gethostbyname_ex'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_socket.cpython-37m-x86_64-linux-gnu.so', '_socket', expected)


@pytest.mark.xfail(strict=True)
def test_sqlite3():
    expected = {'SQLITE_DETACH', 'SQLITE_REINDEX', 'SQLITE_DONE', 'sqlite_version', 'SQLITE_FUNCTION', 'PrepareProtocol', 'SQLITE_DROP_TRIGGER', 'SQLITE_RECURSIVE', 'SQLITE_DROP_INDEX', 'version', 'SQLITE_ATTACH', 'SQLITE_ANALYZE', 'enable_shared_cache', 'SQLITE_CREATE_TEMP_TABLE', 'SQLITE_DROP_TEMP_TRIGGER', 'enable_callback_tracebacks', 'DataError', 'Row', 'PARSE_COLNAMES', 'DatabaseError', 'Connection', 'SQLITE_IGNORE', 'IntegrityError', 'SQLITE_CREATE_TEMP_VIEW', 'SQLITE_DENY', 'Warning', 'OptimizedUnicode', 'SQLITE_CREATE_TEMP_INDEX', 'SQLITE_DROP_TEMP_INDEX', 'adapt', 'converters', 'SQLITE_SAVEPOINT', 'SQLITE_UPDATE', 'Statement', 'SQLITE_READ', 'adapters', 'Cursor', 'Error', 'register_converter', 'SQLITE_CREATE_TEMP_TRIGGER', 'connect', 'SQLITE_TRANSACTION', 'SQLITE_DROP_VIEW', 'SQLITE_DELETE', 'SQLITE_DROP_VTABLE', 'PARSE_DECLTYPES', 'SQLITE_SELECT', 'SQLITE_OK', 'SQLITE_PRAGMA', 'SQLITE_DROP_TEMP_VIEW', 'SQLITE_CREATE_TABLE', 'register_adapter', 'SQLITE_DROP_TEMP_TABLE', 'SQLITE_CREATE_VIEW', 'SQLITE_INSERT', 'InternalError', 'NotSupportedError', 'SQLITE_CREATE_INDEX', 'complete_statement', 'ProgrammingError', 'OperationalError', 'SQLITE_ALTER_TABLE', 'SQLITE_CREATE_VTABLE', 'SQLITE_DROP_TABLE', 'SQLITE_CREATE_TRIGGER', 'Cache', 'InterfaceError'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_sqlite3.cpython-37m-x86_64-linux-gnu.so', '_sqlite3', expected)


def test_ssl():
    expected = {'ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE', 'OP_NO_TLSv1_2', '_DEFAULT_CIPHERS', 'ALERT_DESCRIPTION_INTERNAL_ERROR', 'SSLZeroReturnError', 'SSL_ERROR_WANT_X509_LOOKUP', 'MemoryBIO', 'ALERT_DESCRIPTION_BAD_RECORD_MAC', 'ALERT_DESCRIPTION_BAD_CERTIFICATE', 'ALERT_DESCRIPTION_UNKNOWN_CA', 'ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE', 'OPENSSL_VERSION', 'HOSTFLAG_NO_PARTIAL_WILDCARDS', 'OP_NO_TLSv1_3', 'HOSTFLAG_MULTI_LABEL_WILDCARDS', 'ALERT_DESCRIPTION_CLOSE_NOTIFY', 'ALERT_DESCRIPTION_RECORD_OVERFLOW', 'OPENSSL_VERSION_NUMBER', 'OP_NO_SSLv3', 'VERIFY_CRL_CHECK_CHAIN', 'RAND_add', 'txt2obj', 'get_default_verify_paths', 'err_codes_to_names', 'PROTOCOL_TLS_SERVER', 'SSLWantReadError', 'ALERT_DESCRIPTION_UNRECOGNIZED_NAME', 'HOSTFLAG_ALWAYS_CHECK_SUBJECT', 'ALERT_DESCRIPTION_DECOMPRESSION_FAILURE', 'CERT_REQUIRED', 'ALERT_DESCRIPTION_CERTIFICATE_EXPIRED', 'OP_NO_TLSv1', 'RAND_bytes', 'PROTOCOL_SSLv23', 'SSLSyscallError', 'PROTOCOL_TLS_CLIENT', 'ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION', 'SSL_ERROR_SYSCALL', 'ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE', 'OP_ALL', 'SSL_ERROR_ZERO_RETURN', 'VERIFY_X509_STRICT', 'HAS_TLSv1_2', 'ALERT_DESCRIPTION_NO_RENEGOTIATION', 'PROTOCOL_TLSv1_1', 'SSL_ERROR_WANT_WRITE', '_SSLContext', 'SSLEOFError', 'RAND_status', 'SSLError', 'PROTO_MINIMUM_SUPPORTED', 'SSL_ERROR_EOF', 'ALERT_DESCRIPTION_HANDSHAKE_FAILURE', 'HAS_NPN', 'HAS_SSLv3', 'HAS_ECDH', 'PROTO_TLSv1_1', 'OP_NO_COMPRESSION', 'PROTOCOL_TLSv1', 'ALERT_DESCRIPTION_INSUFFICIENT_SECURITY', 'VERIFY_X509_TRUSTED_FIRST', 'HAS_SNI', 'HAS_TLSv1', 'err_names_to_codes', '_SSLSocket', 'ALERT_DESCRIPTION_CERTIFICATE_UNKNOWN', 'SSLSession', 'OP_NO_TICKET', 'SSLCertVerificationError', 'nid2obj', 'SSL_ERROR_WANT_READ', 'SSLWantWriteError', 'PROTOCOL_TLS', 'OP_NO_SSLv2', 'lib_codes_to_names', 'PROTOCOL_TLSv1_2', 'PROTO_TLSv1_3', 'OP_NO_TLSv1_1', 'HAS_TLS_UNIQUE', 'SSL_ERROR_WANT_CONNECT', 'PROTO_TLSv1_2', 'OP_SINGLE_DH_USE', 'ALERT_DESCRIPTION_DECODE_ERROR', 'SSL_ERROR_SSL', 'OP_NO_RENEGOTIATION', 'ALERT_DESCRIPTION_USER_CANCELLED', 'OP_SINGLE_ECDH_USE', 'HOSTFLAG_SINGLE_LABEL_SUBDOMAINS', 'OP_ENABLE_MIDDLEBOX_COMPAT', 'VERIFY_CRL_CHECK_LEAF', 'ALERT_DESCRIPTION_UNEXPECTED_MESSAGE', 'HAS_ALPN', 'CERT_OPTIONAL', 'RAND_pseudo_bytes', '_test_decode_cert', 'HAS_TLSv1_1', 'ALERT_DESCRIPTION_ILLEGAL_PARAMETER', '_OPENSSL_API_VERSION', 'PROTO_TLSv1', 'OP_CIPHER_SERVER_PREFERENCE', 'VERIFY_DEFAULT', 'OPENSSL_VERSION_INFO', 'ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE', 'HAS_TLSv1_3', 'ALERT_DESCRIPTION_CERTIFICATE_REVOKED', 'HOSTFLAG_NO_WILDCARDS', 'SSL_ERROR_INVALID_ERROR_CODE', 'ALERT_DESCRIPTION_ACCESS_DENIED', 'ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY', 'HOSTFLAG_NEVER_CHECK_SUBJECT', 'PROTO_SSLv3', 'HAS_SSLv2', 'PROTO_MAXIMUM_SUPPORTED', 'CERT_NONE', 'ALERT_DESCRIPTION_PROTOCOL_VERSION', 'ALERT_DESCRIPTION_DECRYPT_ERROR'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_ssl.cpython-37m-x86_64-linux-gnu.so', '_ssl', expected)


def test_struct():
    expected = {'pack_into', 'calcsize', 'Struct', 'iter_unpack', '_clearcache', 'unpack', 'pack', 'unpack_from', 'error'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_struct.cpython-37m-x86_64-linux-gnu.so', '_struct', expected)


def test_testbuffer():
    expected = {'ND_GETBUF_FAIL', 'PyBUF_ND', 'ND_SCALAR', 'ND_VAREXPORT', 'get_pointer', 'cmp_contig', 'PyBUF_WRITABLE', 'PyBUF_SIMPLE', 'PyBUF_FORMAT', 'PyBUF_CONTIG', 'ND_MAX_NDIM', 'PyBUF_C_CONTIGUOUS', 'ND_WRITABLE', 'get_contiguous', 'ND_FORTRAN', 'py_buffer_to_contiguous', 'staticarray', 'PyBUF_WRITE', 'PyBUF_F_CONTIGUOUS', 'ndarray', 'PyBUF_STRIDED', 'get_sizeof_void_p', 'PyBUF_STRIDES', 'PyBUF_FULL', 'ND_REDIRECT', 'PyBUF_INDIRECT', 'slice_indices', 'PyBUF_FULL_RO', 'is_contiguous', 'ND_PIL', 'PyBUF_RECORDS', 'PyBUF_READ', 'PyBUF_CONTIG_RO', 'PyBUF_RECORDS_RO', 'ND_GETBUF_UNDEFINED', 'PyBUF_STRIDED_RO', 'PyBUF_ANY_CONTIGUOUS'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_testbuffer.cpython-37m-x86_64-linux-gnu.so', '_testbuffer', expected)


def test_testcapi():
    expected = {'FLT_MAX', 'traceback_print', 'raise_SIGINT_then_send_None', 'LLONG_MAX', 'UCHAR_MAX', 'parse_tuple_and_keywords', 'PY_SSIZE_T_MIN', 'pymem_getallocatorsname', 'USHRT_MAX', 'tracemalloc_track', 'PyTime_AsMicroseconds', 'getargs_k', 'FLT_MIN', 'SIZEOF_TIME_T', 'test_long_as_size_t', 'docstring_no_signature', 'get_global_config', 'test_long_and_overflow', 'test_buildvalue_N', 'pymarshal_write_long_to_file', 'tracemalloc_untrack', 'docstring_with_invalid_signature2', 'test_L_code', 'docstring_with_signature_and_extra_newlines', 'return_null_without_error', 'test_long_numbits', 'test_Z_code', 'set_nomemory', 'PY_SSIZE_T_MAX', 'test_long_as_unsigned_long_long_mask', 'pymarshal_read_last_object_from_file', 'no_docstring', 'datetime_check_time', 'DBL_MAX', 'codec_incrementalencoder', 'make_exception_with_doc', 'GenericAlias', 'matmulType', 'get_mapping_values', 'call_in_temporary_c_thread', 'test_string_to_double', 'getargs_positional_only_and_keywords', '_test_thread_state', 'code_newempty', 'dict_get_version', 'getargs_C', 'getargs_Y', 'test_incref_decref_API', 'hamt', '_pending_threadfunc', 'run_in_subinterp', 'test_xincref_doesnt_leak', 'LONG_MIN', 'PyTime_AsTimespec', 'datetime_check_tzinfo', 'awaitType', 'INT_MAX', 'getargs_y', 'get_kwargs', 'getargs_H', 'CHAR_MAX', 'LLONG_MIN', 'argparsing', 'pymem_buffer_overflow', 'test_datetime_capi', 'test_pythread_tss_key_state', 'getargs_i', 'raise_exception', 'get_main_config', 'getargs_w_star', 'stack_pointer', 'PyTime_FromSecondsObject', 'pyobject_malloc_without_gil', 'test_from_contiguous', 'test_u_code', 'instancemethod', 'getargs_l', 'test_long_as_double', 'LONG_MAX', 'getargs_keyword_only', 'unicode_encodedecimal', 'test_config', 'test_dict_iteration', 'getargs_L', 'test_null_strings', 'getargs_K', 'getargs_u_hash', 'create_cfunction', 'W_STOPCODE', 'ULONG_MAX', 'unicode_findchar', 'pymem_malloc_without_gil', 'INT_MIN', 'getargs_D', 'getargs_y_star', 'docstring_with_signature_but_no_doc', 'SIZEOF_PYGC_HEAD', 'getargs_U', 'test_string_from_format', 'raise_signal', 'getargs_tuple', 'PyTime_AsTimeval', 'getargs_B', 'pymem_api_misuse', 'codec_incrementaldecoder', 'dict_getitem_knownhash', 'getargs_c', 'test_sizeof_c_types', 'pymarshal_read_long_from_file', 'get_timezone_utc_capi', 'getargs_I', 'getargs_n', 'SHRT_MAX', 'test_empty_argparse', 'datetime_check_date', 'pytime_object_to_timeval', 'test_pymem_setallocators', 'getargs_Z', 'test_pep3118_obsolete_write_locks', 'get_args', 'getargs_s_hash', 'docstring_with_signature', 'unicode_transformdecimaltoascii', 'PyTime_FromSeconds', 'unicode_aswidechar', 'test_long_long_and_overflow', 'pyobject_uninitialized', 'test_longlong_api', 'PyTime_AsMilliseconds', 'docstring_empty', 'pymarshal_read_short_from_file', 'pytime_object_to_timespec', 'get_recursion_depth', 'SHRT_MIN', 'test_pymem_alloc0', 'test_pyobject_setallocators', 'getargs_u', 'getbuffer_with_null_view', 'getargs_p', '_test_structmembersType', 'error', 'pyobject_forbidden_bytes', 'getargs_Z_hash', 'getargs_y_hash', 'tracemalloc_get_traceback', 'getargs_s', 'getargs_z_star', 'getargs_es', 'pyobject_is_freed', 'ULLONG_MAX', 'test_k_code', 'test_unicode_compare_with_ascii', 'test_widechar', 'datetime_check_datetime', 'getargs_es_hash', 'CHAR_MIN', 'DBL_MIN', 'get_timezones_offset_zero', 'raise_memoryerror', 'test_lazy_hash_inheritance', 'get_mapping_keys', 'test_capsule', 'pyobject_freed', 'remove_mem_hooks', 'Generic', 'pyobject_fastcall', 'pyobject_fastcalldict', 'test_xdecref_doesnt_leak', 'the_number_three', 'make_memoryview_from_NULL_pointer', 'pyobject_fastcallkeywords', 'set_exc_info', 'unicode_aswidecharstring', 'get_core_config', 'test_long_api', 'exception_print', 'docstring_with_invalid_signature', 'unicode_legacy_string', 'datetime_check_delta', 'get_mapping_items', 'RecursingInfinitelyError', 'WITH_PYMALLOC', 'unicode_asucs4', 'getargs_h', 'docstring_with_signature_with_defaults', 'pytime_object_to_time_t', 'pymarshal_write_object_to_file', 'test_pymem_setrawallocators', 'UINT_MAX', 'getargs_et', 'getargs_d', 'getargs_s_star', 'getargs_z', 'getargs_f', 'PyTime_AsSecondsDouble', 'getargs_et_hash', 'getargs_S', 'with_tp_del', 'unicode_copycharacters', 'set_errno', 'getargs_keywords', 'profile_int', 'return_result_with_error', 'make_timezones_capi', 'getargs_b', 'getargs_z_hash', 'pymarshal_read_object_from_file', 'dict_hassplittable', 'test_incref_doesnt_leak', 'test_list_api', 'test_s_code', 'crash_no_current_thread', 'test_with_docstring', 'test_decref_doesnt_leak'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_testcapi.cpython-37m-x86_64-linux-gnu.so', '_testcapi', expected)


def test_testimportmultiple():
    expected = set()
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_testimportmultiple.cpython-37m-x86_64-linux-gnu.so', '_testimportmultiple', expected)


@pytest.mark.xfail(strict=True)
def test_testmultiphase():
    expected = {'call_state_registration_func', 'Str', 'Example', 'int_const', 'str_const', 'foo', 'error'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_testmultiphase.cpython-37m-x86_64-linux-gnu.so', '_testmultiphase', expected)


def test_tkinter():
    expected = {'Tcl_Obj', 'IDLE_EVENTS', 'setbusywaitinterval', 'WINDOW_EVENTS', 'TkttType', 'TclError', 'DONT_WAIT', 'TK_VERSION', 'getbusywaitinterval', '_flatten', 'TkappType', 'EXCEPTION', 'WRITABLE', 'TIMER_EVENTS', 'TCL_VERSION', 'ALL_EVENTS', 'create', 'READABLE', 'FILE_EVENTS'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_tkinter.cpython-37m-x86_64-linux-gnu.so', '_tkinter', expected)


def test_xxtestfuzz():
    expected = {'run'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/_xxtestfuzz.cpython-37m-x86_64-linux-gnu.so', '_xxtestfuzz', expected)


@pytest.mark.xfail(strict=True)
def test_array():
    expected = {'typecodes', 'ArrayType', '_array_reconstructor', 'array'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/array.cpython-37m-x86_64-linux-gnu.so', 'array', expected)


def test_audioop():
    expected = {'cross', 'rms', 'findfit', 'alaw2lin', 'maxpp', 'ulaw2lin', 'add', 'lin2lin', 'tostereo', 'bias', 'lin2alaw', 'findfactor', 'minmax', 'tomono', 'adpcm2lin', 'lin2ulaw', 'avg', 'reverse', 'getsample', 'lin2adpcm', 'error', 'avgpp', 'findmax', 'ratecv', 'byteswap', 'max', 'mul'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/audioop.cpython-37m-x86_64-linux-gnu.so', 'audioop', expected)


def test_fcntl():
    expected = {'F_GETOWN', 'I_SRDOPT', 'I_GETBAND', 'LOCK_UN', 'flock', 'F_GETSIG', 'lockf', 'I_NREAD', 'F_GETLK', 'F_EXLCK', 'F_NOTIFY', 'FD_CLOEXEC', 'DN_CREATE', 'ioctl', 'I_PUNLINK', 'I_CANPUT', 'I_FLUSHBAND', 'DN_DELETE', 'F_SETFL', 'F_SETLKW64', 'I_CKBAND', 'I_PEEK', 'F_UNLCK', 'I_POP', 'I_PUSH', 'DN_RENAME', 'F_SETLK64', 'LOCK_WRITE', 'fcntl', 'F_SETSIG', 'LOCK_SH', 'I_ATMARK', 'I_PLINK', 'I_RECVFD', 'I_GWROPT', 'F_SETLKW', 'I_LOOK', 'F_DUPFD', 'LOCK_EX', 'F_SETLEASE', 'LOCK_NB', 'DN_MODIFY', 'F_SETFD', 'F_SHLCK', 'F_GETFL', 'FASYNC', 'F_DUPFD_CLOEXEC', 'I_FIND', 'I_SENDFD', 'DN_MULTISHOT', 'I_SETSIG', 'I_FDINSERT', 'I_UNLINK', 'I_LIST', 'F_GETLEASE', 'F_SETLK', 'F_RDLCK', 'F_GETLK64', 'DN_ACCESS', 'I_SETCLTIME', 'I_LINK', 'LOCK_MAND', 'LOCK_READ', 'I_GRDOPT', 'F_SETOWN', 'F_GETFD', 'I_SWROPT', 'DN_ATTRIB', 'F_WRLCK', 'I_STR', 'I_GETCLTIME', 'LOCK_RW', 'I_GETSIG', 'I_FLUSH'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/fcntl.cpython-37m-x86_64-linux-gnu.so', 'fcntl', expected)


def test_grp():
    expected = {'struct_group', 'getgrall', 'getgrnam', 'getgrgid'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/grp.cpython-37m-x86_64-linux-gnu.so', 'grp', expected)


def test_ossaudiodev():
    expected = {'SNDCTL_DSP_SETDUPLEX', 'SNDCTL_DSP_GETTRIGGER', 'SNDCTL_DSP_GETODELAY', 'SNDCTL_MIDI_PRETIME', 'SNDCTL_TMR_START', 'SNDCTL_COPR_WCODE', 'AFMT_A_LAW', 'AFMT_MPEG', 'SNDCTL_DSP_SETFRAGMENT', 'SNDCTL_COPR_RDATA', 'SOUND_MIXER_NRDEVICES', 'SNDCTL_DSP_POST', 'SNDCTL_DSP_STEREO', 'SOUND_MIXER_OGAIN', 'SOUND_MIXER_CD', 'SNDCTL_TMR_STOP', 'openmixer', 'SNDCTL_DSP_SUBDIVIDE', 'AFMT_MU_LAW', 'SOUND_MIXER_DIGITAL1', 'error', 'SNDCTL_COPR_RCODE', 'AFMT_AC3', 'SOUND_MIXER_DIGITAL2', 'SNDCTL_FM_LOAD_INSTR', 'SNDCTL_DSP_SPEED', 'SNDCTL_DSP_GETBLKSIZE', 'SOUND_MIXER_DIGITAL3', 'SOUND_MIXER_LINE3', 'SNDCTL_SEQ_PERCMODE', 'SOUND_MIXER_LINE2', 'SNDCTL_DSP_CHANNELS', 'SOUND_MIXER_IGAIN', 'SOUND_MIXER_IMIX', 'AFMT_S8', 'SNDCTL_SYNTH_REMOVESAMPLE', 'AFMT_U16_LE', 'SNDCTL_SEQ_NRSYNTHS', 'SNDCTL_DSP_GETISPACE', 'SNDCTL_DSP_BIND_CHANNEL', 'SNDCTL_MIDI_MPUMODE', 'SNDCTL_DSP_GETCHANNELMASK', 'SNDCTL_COPR_RUN', 'SNDCTL_SEQ_RESETSAMPLES', 'SOUND_MIXER_VOLUME', 'SOUND_MIXER_LINE', 'SNDCTL_DSP_GETOPTR', 'SNDCTL_SEQ_GETTIME', 'SNDCTL_COPR_HALT', 'SNDCTL_TMR_CONTINUE', 'SNDCTL_TMR_SOURCE', 'SNDCTL_DSP_SETSYNCRO', 'SNDCTL_DSP_GETIPTR', 'AFMT_U16_BE', 'AFMT_U8', 'SNDCTL_TMR_SELECT', 'SNDCTL_DSP_SAMPLESIZE', 'SOUND_MIXER_PCM', 'SNDCTL_SYNTH_ID', 'AFMT_S16_BE', 'SOUND_MIXER_BASS', 'SNDCTL_DSP_RESET', 'SNDCTL_DSP_PROFILE', 'AFMT_S16_NE', 'SNDCTL_MIDI_MPUCMD', 'AFMT_IMA_ADPCM', 'SNDCTL_COPR_RCVMSG', 'SNDCTL_COPR_LOAD', 'SOUND_MIXER_RADIO', 'SOUND_MIXER_PHONEOUT', 'AFMT_S16_LE', 'SNDCTL_FM_4OP_ENABLE', 'SNDCTL_MIDI_INFO', 'SNDCTL_DSP_SETFMT', 'SNDCTL_SYNTH_INFO', 'SNDCTL_SEQ_NRMIDIS', 'SNDCTL_DSP_NONBLOCK', 'SNDCTL_SEQ_OUTOFBAND', 'SNDCTL_SEQ_GETOUTCOUNT', 'SNDCTL_DSP_MAPINBUF', 'SOUND_MIXER_VIDEO', 'SNDCTL_DSP_GETFMTS', 'SOUND_MIXER_TREBLE', 'SOUND_MIXER_ALTPCM', 'SNDCTL_SEQ_RESET', 'SNDCTL_DSP_GETOSPACE', 'SNDCTL_TMR_TEMPO', 'SNDCTL_COPR_WDATA', 'OSSAudioError', 'SNDCTL_SEQ_CTRLRATE', 'SOUND_MIXER_RECLEV', 'SNDCTL_TMR_TIMEBASE', 'SNDCTL_DSP_MAPOUTBUF', 'SNDCTL_DSP_GETCAPS', 'SNDCTL_COPR_SENDMSG', 'SNDCTL_TMR_METRONOME', 'control_names', 'SOUND_MIXER_SYNTH', 'SNDCTL_DSP_GETSPDIF', 'SNDCTL_SYNTH_CONTROL', 'SOUND_MIXER_MIC', 'SOUND_MIXER_PHONEIN', 'SNDCTL_COPR_RESET', 'SNDCTL_DSP_SETTRIGGER', 'SNDCTL_SEQ_SYNC', 'SOUND_MIXER_MONITOR', 'SNDCTL_SEQ_THRESHOLD', 'SOUND_MIXER_SPEAKER', 'SNDCTL_SYNTH_MEMAVL', 'SNDCTL_SEQ_GETINCOUNT', 'control_labels', 'SOUND_MIXER_LINE1', 'SNDCTL_DSP_SYNC', 'SNDCTL_SEQ_PANIC', 'AFMT_QUERY', 'SNDCTL_DSP_SETSPDIF', 'SNDCTL_SEQ_TESTMIDI', 'open'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/ossaudiodev.cpython-37m-x86_64-linux-gnu.so', 'ossaudiodev', expected)


def test_readline():
    expected = {'get_begidx', 'get_completion_type', '_READLINE_LIBRARY_VERSION', 'set_startup_hook', 'get_history_length', 'set_auto_history', 'write_history_file', 'get_current_history_length', 'append_history_file', 'add_history', 'insert_text', 'read_init_file', 'get_history_item', 'get_completer_delims', 'get_line_buffer', 'get_endidx', 'set_pre_input_hook', 'set_completer', 'set_history_length', 'redisplay', 'remove_history_item', '_READLINE_RUNTIME_VERSION', '_READLINE_VERSION', 'get_completer', 'parse_and_bind', 'replace_history_item', 'read_history_file', 'set_completer_delims', 'clear_history', 'set_completion_display_matches_hook'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/readline.cpython-37m-x86_64-linux-gnu.so', 'readline', expected)


def test_resource():
    expected = {'RLIMIT_STACK', 'RLIMIT_NICE', 'RUSAGE_THREAD', 'getrlimit', 'RUSAGE_CHILDREN', 'struct_rusage', 'RLIMIT_OFILE', 'RLIMIT_CPU', 'RLIMIT_RTPRIO', 'setrlimit', 'getrusage', 'RLIMIT_DATA', 'RLIMIT_MSGQUEUE', 'RLIM_INFINITY', 'RLIMIT_MEMLOCK', 'RLIMIT_RSS', 'RLIMIT_NPROC', 'getpagesize', 'RLIMIT_CORE', 'RLIMIT_FSIZE', 'RLIMIT_AS', 'RLIMIT_SIGPENDING', 'RLIMIT_NOFILE', 'error', 'RUSAGE_SELF'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/resource.cpython-37m-x86_64-linux-gnu.so', 'resource', expected)


def test_spwd():
    expected = {'getspall', 'getspnam', 'struct_spwd'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/spwd.cpython-37m-x86_64-linux-gnu.so', 'spwd', expected)


def test_syslog():
    expected = {'LOG_PID', 'LOG_LOCAL0', 'LOG_MAIL', 'LOG_LOCAL7', 'LOG_CRON', 'LOG_NOWAIT', 'syslog', 'LOG_LOCAL2', 'openlog', 'LOG_MASK', 'LOG_AUTH', 'LOG_LPR', 'LOG_INFO', 'LOG_USER', 'LOG_WARNING', 'LOG_DAEMON', 'LOG_LOCAL3', 'LOG_LOCAL4', 'LOG_EMERG', 'LOG_CONS', 'LOG_SYSLOG', 'setlogmask', 'LOG_DEBUG', 'LOG_NOTICE', 'LOG_UPTO', 'LOG_LOCAL6', 'LOG_CRIT', 'LOG_ODELAY', 'closelog', 'LOG_ERR', 'LOG_PERROR', 'LOG_NDELAY', 'LOG_LOCAL5', 'LOG_AUTHPRIV', 'LOG_LOCAL1', 'LOG_KERN', 'LOG_UUCP', 'LOG_ALERT', 'LOG_NEWS'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/syslog.cpython-37m-x86_64-linux-gnu.so', 'syslog', expected)


@pytest.mark.xfail(strict=True)
def test_termios():
    expected = {'ICANON', 'CSTART', 'B460800', 'TIOCMGET', 'BSDLY', 'TCSETS', 'CINTR', 'TIOCSERGWILD', 'B230400', 'TIOCGSOFTCAR', 'CQUIT', 'VEOL', 'TIOCM_RNG', 'VEOL2', 'TIOCSERGETLSR', 'INLCR', 'TCSETSF', 'ONLRET', 'TCIOFLUSH', 'B2000000', 'BS0', 'NCC', 'TIOCGPGRP', 'TIOCM_RI', 'TIOCSERSETMULTI', 'CDSUSP', 'FIOASYNC', 'CR0', 'OFILL', 'NL0', 'N_SLIP', 'CS8', 'TIOCSERCONFIG', 'TIOCM_SR', 'IUCLC', 'B300', 'TAB0', 'BS1', 'VMIN', 'CIBAUD', 'CSIZE', 'TIOCM_DTR', 'PARENB', 'IXANY', 'TIOCSER_TEMT', 'B9600', 'TCION', 'VKILL', 'TCSANOW', 'IOCSIZE_SHIFT', 'TIOCPKT_DATA', 'OLCUC', 'TIOCPKT_NOSTOP', 'N_TTY', 'B4800', 'N_PPP', 'PARMRK', 'CREAD', 'TABDLY', 'TIOCEXCL', 'OCRNL', 'TIOCM_RTS', 'CS6', 'TIOCSPGRP', 'VSTART', 'TIOCSERSWILD', 'B19200', 'ECHOKE', 'TCOFLUSH', 'ECHONL', 'TIOCGSERIAL', 'TIOCNXCL', 'TCSAFLUSH', 'B500000', 'B110', 'B200', 'TIOCSTI', 'IGNPAR', 'TIOCSSOFTCAR', 'ECHO', 'ISTRIP', 'B2500000', 'TIOCPKT_STOP', 'FLUSHO', 'IGNBRK', 'TIOCPKT_DOSTOP', 'TCSETSW', 'CRPRNT', 'TCSETAW', 'PARODD', 'TIOCSCTTY', 'B1000000', 'VDISCARD', 'ECHOK', 'CSUSP', 'TIOCINQ', 'tcsetattr', 'tcsendbreak', 'TIOCSETD', 'tcdrain', 'B3500000', 'VSTOP', 'TIOCM_DSR', 'tcgetattr', 'ONLCR', 'VERASE', 'TCOOFF', 'TIOCMBIC', 'TIOCM_ST', 'TCSETA', 'TIOCSLCKTRMIOS', 'TCOON', 'TIOCPKT_FLUSHREAD', 'ECHOPRT', 'TIOCGETD', 'FIONBIO', 'TIOCNOTTY', 'CLOCAL', 'TOSTOP', 'TIOCSWINSZ', 'FF1', 'VLNEXT', 'TIOCSSERIAL', 'VTDLY', 'CRDLY', 'B2400', 'IXOFF', 'HUPCL', 'CR2', 'B134', 'FIONREAD', 'CRTSCTS', 'TCIOFF', 'TIOCMIWAIT', 'TIOCOUTQ', 'error', 'TIOCPKT_FLUSHWRITE', 'B1152000', 'IOCSIZE_MASK', 'TCIFLUSH', 'ICRNL', 'TAB1', 'CKILL', 'TIOCGLCKTRMIOS', 'CERASE', 'CLNEXT', 'IGNCR', 'VSUSP', 'CBAUD', 'CS7', 'B38400', 'ONOCR', 'TIOCMSET', 'TIOCSERGETMULTI', 'BRKINT', 'B57600', 'B1200', 'CR3', 'IEXTEN', 'B3000000', 'TIOCGWINSZ', 'tcflush', 'N_MOUSE', 'VWERASE', 'TIOCM_CAR', 'INPCK', 'B150', 'TCFLSH', 'B600', 'TCXONC', 'NOFLSH', 'CFLUSH', 'VSWTC', 'ECHOCTL', 'FIOCLEX', 'B921600', 'NCCS', 'FIONCLEX', 'tcflow', 'TIOCM_CD', 'TIOCSERGSTRUCT', 'ISIG', 'TCSADRAIN', 'TCGETS', 'TIOCMBIS', 'TIOCPKT', 'ECHOE', 'TIOCM_CTS', 'TCSBRKP', 'NL1', 'TIOCLINUX', 'FFDLY', 'VREPRINT', 'NLDLY', 'B50', 'CR1', 'CEOT', 'B4000000', 'CSTOP', 'VEOF', 'CWERASE', 'VSWTCH', 'CEOF', 'N_STRIP', 'CS5', 'VT1', 'FF0', 'EXTB', 'OPOST', 'TIOCCONS', 'TCSBRK', 'B1500000', 'VINTR', 'IXON', 'VTIME', 'XCASE', 'XTABS', 'TCGETA', 'TIOCPKT_START', 'CSTOPB', 'TAB3', 'VT0', 'B115200', 'B576000', 'TAB2', 'TIOCM_LE', 'IMAXBEL', 'TIOCGICOUNT', 'OFDEL', 'PENDIN', 'TCSETAF', 'B0', 'B75', 'CEOL', 'VQUIT', 'B1800', 'CBAUDEX', 'EXTA'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/termios.cpython-37m-x86_64-linux-gnu.so', 'termios', expected)


def test_unicodedata():
    expected = {'ucd_3_2_0', 'decimal', 'UCD', 'unidata_version', 'east_asian_width', 'ucnhash_CAPI', 'normalize', 'name', 'bidirectional', 'decomposition', 'combining', 'mirrored', 'lookup', 'category', 'numeric', 'digit'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/unicodedata.cpython-37m-x86_64-linux-gnu.so', 'unicodedata', expected)


@pytest.mark.xfail(strict=True)
def test_xxlimited():
    expected = {'Xxo', 'Null', 'Str', 'roj', 'new', 'error', 'foo'}
    compare('/home/cburr/miniconda3/lib/python3.7/lib-dynload/xxlimited.cpython-37m-x86_64-linux-gnu.so', 'xxlimited', expected)

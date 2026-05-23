import os
import sys
import pytest
from src.utils import Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('dyld_insert_libraries', 'main.c'), os.path.join('dyld_insert_libraries', 'dep.c')],
        result=Result.executable,
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler):
    # Compile the file that contains the function being mocked
    dep = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('dyld_insert_libraries', 'dep.c')],
        result=Result.dynamic,
    ))

    # Compile file containing mock symbol
    mock = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('dyld_insert_libraries', 'mock.c'), dep],
        result=Result.dynamic,
    ))

    # Compile the rest of the source files (one) separately
    main = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('dyld_insert_libraries', 'main.c'), dep],
        result=Result.dynamic,
    ))

    # Compile the final executable, because we've added `main` and `dep` as files
    # the linker knows *what* files to look for. The linker flag `-rpath` then
    # tells the linker *where* to look at runtime to find these files.
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[main, dep],
        result=Result.executable,
    ))

    # Mocked behavior: DYLD_INSERT_LIBRARIES loads our interpose library,
    # which replaces the targeted pointers inside the two-level namespace.
    code, out, err = run(executable, env=dict(DYLD_INSERT_LIBRARIES=mock))
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'


@pytest.fixture(autouse=True)
def dyld_insert_libraries_is_a_mac_thing():
    if sys.platform != 'darwin':
        pytest.skip('DYLD_INSERT_LIBRARIES is a mac thing')

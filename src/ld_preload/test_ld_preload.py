import os
import sys
import pytest
from src.utils import Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('ld_preload', 'main.c'), os.path.join('ld_preload', 'dep.c')],
        result=Result.executable,
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler):
    # Compile file containing mock symbol
    mock = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('ld_preload', 'mock.c')],
        result=Result.dynamic,
        flags=['-ldl'],  # Mock uses `dlsym` to call real function
    ))

    # Compile all source files separately
    dep = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('ld_preload', 'dep.c')],
        result=Result.dynamic,
    ))

    # Compile the final executable, because we've added `main` and `dep` as files
    # the linker knows *what* files to look for. The linker flag `-rpath` then
    # tells the linker *where* to look at runtime to find these files.
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('ld_preload', 'main.c'), dep],
        result=Result.executable,
        flags=[f'-Wl,-rpath={os.path.dirname(dep)}'],
    ))

    # Mocked behaviour, `LD_PRELOAD` puts us in front of the line when the symbols
    # are resolved dynamically
    code, out, err = run(executable, env=dict(LD_PRELOAD=mock))
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'


@pytest.fixture(autouse=True)
def ld_preload_is_a_linux_thing():
    if not sys.platform.startswith('linux'):
        pytest.skip('LD_PRELOAD is a linux thing')

import os
from src.utils import Macro, Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('function_pointers', 'main.c'), os.path.join('function_pointers', 'dep.c')],
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
        files=[os.path.join('function_pointers', 'mock.c')],
        result=Result.object,
    ))

    # Compile the final executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('function_pointers', 'main.c'), os.path.join('function_pointers', 'dep.c'), mock],
        result=Result.executable,
        macros=[Macro(name='main', value='real_main')],
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'

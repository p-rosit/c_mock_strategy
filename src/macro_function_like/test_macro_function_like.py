import os
from src.utils import Macro, Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('macro_function_like', 'main.c'), os.path.join('macro_function_like', 'dep.c')],
        result=Result.executable,
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler):
    # Macro which will replace all calls of symbol with mock
    m = Macro(name='external_func(a)', value='mock_external_func(a)')

    # Compile executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[
            os.path.join('macro_function_like', 'main.c'),
            os.path.join('macro_function_like', 'dep.c'),
            os.path.join('macro_function_like', 'mock.c'),
        ],
        result=Result.executable,
        macros=[m],
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'

import os
from src.utils import Macro, Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('macro_object_like', 'main.c'), os.path.join('macro_object_like', 'dep.c')],
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
        files=[os.path.join('macro_object_like', 'mock.c')],
        result=Result.object,
    ))

    # Macro which will replace all calls of symbol with mock
    m = Macro(name='external_func', value='mock_external_func')

    # Compile all files (one) which do not contain the definition of the symbol
    # that's being replaced, use the macro_object_like to replace all calls with the mock
    main = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('macro_object_like', 'main.c')],
        result=Result.object,
        macros=[m],
    ))

    # Compile the file containing definition of the symbol without the macro_object_like.
    # Otherwise the definition will be renamed...
    dep = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('macro_object_like', 'dep.c')],
        result=Result.object,
    ))

    # Compile the final executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[main, dep, mock],
        result=Result.executable,
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'

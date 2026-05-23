import os
import sys
import subprocess
import pytest
from src.utils import Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('linker_wrap', 'main.c'), os.path.join('linker_wrap', 'dep.c')],
        result=Result.executable,
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler):
    # Compile all files separately
    files = []
    for f in ['mock.c', 'main.c', 'dep.c']:
        files.append(compile(CompileCommand(
            compiler=compiler,
            files=[os.path.join('linker_wrap', f)],
            result=Result.object,
        )))

    # Compile the final executable, you could compile the object files with
    # whatever compiler you prefer and then link with any linker that supports
    # wrapping function calls like `--wrap` does. Here we pass linker flags
    # through the compiler and use the default linker
    executable = compile(CompileCommand(
        compiler=compiler,
        files=files,
        result=Result.executable,
        flags=['-Wl,--wrap=external_func'],
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'


@pytest.fixture(autouse=True)
def skip_if_linker_incompatible(compiler):
    if compiler == 'gcc':
        return  # Honestly it's too complicated and I don't care that much
    if compiler not in ['gcc', 'clang']:
        pytest.skip(f'Default linker to {compiler} (most likely) does not support `--wrap`')

    p = subprocess.Popen(
        f'{compiler} -### {os.path.join(os.path.dirname(__file__), "main.c")}',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )
    _, err = p.communicate()

    linker_command = err.splitlines()[-1]
    _, linker = os.path.split(linker_command.split('"')[1])

    if linker != 'ld' or sys.platform == 'darwin':
        pytest.skip(f'Default linker to {compiler} (most likely) does not support `--wrap`')

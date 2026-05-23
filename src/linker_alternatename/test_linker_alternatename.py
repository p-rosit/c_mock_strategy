import os
import pytest
from src.utils import Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('linker_alternatename', 'main.c'), os.path.join('linker_alternatename', 'dep.c')],
        result=Result.executable,
        flags=[
            '/link',  # the `/link` (all lowercase) needs to be at the end of the command, that's how `CompileCommand` builds the command string
            '/ALTERNATENAME:_external_func=_real_external_func',
            '/ALTERNATENAME:_internal_func=_real_internal_func',
        ],
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler):
    # Compile the final executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[
            os.path.join('linker_alternatename', 'main.c'),
            os.path.join('linker_alternatename', 'dep.c'),
            os.path.join('linker_alternatename', 'mock.c'),
        ],
        result=Result.executable,
        flags=[
            '/link',  # the `/link` (all lowercase) needs to be at the end of the command, that's how `CompileCommand` builds the command string
            '/ALTERNATENAME:_external_func=_mock_external_func',  # Mock `external_func`
            '/ALTERNATENAME:_internal_func=_real_internal_func',  # Don't mock `internal_func`
        ],
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'


@pytest.fixture(autouse=True)
def skip_if_linker_incompatible(compiler):
    if compiler not in ['cl', 'clang-cl']:
        pytest.skip(f'Default linker to {compiler} (most likely) does not support `/alternatename`')

import os
import pathlib
import subprocess
import pytest
from src.utils import Result, compile, run, CompileCommand


def test_default(compiler):
    # Compile original executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('objcopy', 'main.c'), os.path.join('objcopy', 'dep.c')],
        result=Result.executable,
    ))

    # Normal behaviour
    code, out, err = run(executable)
    assert 10 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert '' == err, f'Got {repr(err)}'


def test_mock(compiler, objcopy):
    # Compile file containing mock symbol
    mock = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('objcopy', 'mock.c')],
        result=Result.object,
    ))

    # Compile source files separately
    main = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('objcopy', 'main.c')],
        result=Result.object,
    ))
    dep = compile(CompileCommand(
        compiler=compiler,
        files=[os.path.join('objcopy', 'dep.c')],
        result=Result.object,
    ))

    # Use objcopy to redirect function calls

    # Remap to mock symbol in all source files that don't contain the definition
    main_path, main_name = os.path.split(main)
    remapped_main = os.path.join(main_path, f'remapped_{main_name}')

    if os.name == 'nt':
        # When compiling 32bit windows executable (i guess the default???)
        # the compiler will prefix symbols with an underscore
        remap = '_external_func=_wrap_external_func'
    else:
        remap = 'external_func=wrap_external_func'

    p = subprocess.Popen(
        [objcopy, '--redefine-sym', remap, main, remapped_main],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        text=True,
    )
    out, err = p.communicate()

    # Link the final executable
    executable = compile(CompileCommand(
        compiler=compiler,
        files=[remapped_main, dep, mock],
        result=Result.executable,
    ))

    # Mocked behaviour
    code, out, err = run(executable)
    assert 5 == code, f'Got {code}'
    assert '' == out, f'Got {repr(out)}'
    assert 'Real result: 10' == err.strip(), f'Got {repr(err)}'


@pytest.fixture(params=['objcopy', 'llvm-objcopy'])
def objcopy(request):
    path_env = os.environ.get("PATH", "")
    directories = [pathlib.Path(d) for d in path_env.split(os.pathsep) if d]

    found_binaries = set()
    for directory in directories:
        if not directory.is_dir():
            continue

        try:
            for entry in directory.iterdir():
                # Match prefix, ensure it's a file, and verify it's executable
                if entry.name.startswith(request.param) and entry.is_file():
                    if os.access(entry, os.X_OK):
                        # Resolve symlinks to avoid duplicate reporting (e.g., /usr/bin/llvm-objcopy -> llvm-objcopy-18)
                        found_binaries.add(entry.resolve())
        except PermissionError:
            # Skip directories we don't have read access to
            continue

    if not found_binaries:
        pytest.skip(f'Objcopy "{request.param}" not available')

    return next(iter(found_binaries))

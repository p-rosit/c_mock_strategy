import pytest
import tempfile
import shutil


def pytest_addoption(parser):
    parser.addoption('--compiler', action='store', default='gcc,clang,cl,clang-cl,tcc')


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--compiler') is None:
        raise ValueError('Missing compiler, specify with e.g. `--compiler gcc,clang`')

    compiler_str = metafunc.config.getoption('--compiler').strip().split(',')
    compilers = [s.strip() for s in compiler_str if compiler_str]
    if not compilers:
        raise ValueError('Compiler option specified but no arguments supplied, use e.g. `--compiler gcc,clang`')

    metafunc.parametrize('compiler', compilers)


@pytest.fixture(autouse=True, scope='session')
def temp_directory():
    from src import utils
    name = tempfile.mkdtemp()
    utils.temp_directory = name
    yield name
    shutil.rmtree(name)


@pytest.fixture(autouse=True)
def check_compiler(compiler):
    if not shutil.which(compiler):
        pytest.skip(f'Compiler {compiler} not available')

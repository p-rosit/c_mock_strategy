from typing import List, Any, Optional
import os
import sys
import enum
import dataclasses
import subprocess


temp_directory: Optional[str] = None


@dataclasses.dataclass
class Macro:
    name: str
    value: Optional[Any] = None

    def as_flag(self, compiler: str) -> str:
        if compiler in ['gcc', 'clang', 'tcc']:
            return f'-D{self.name}={self.value or ""}'
        elif compiler in ['cl', 'clang-cl']:
            return f'/D{self.name}={self.value or ""}'
        raise NotImplementedError(f'Unknown compiler: "{compiler}"')


class Result(enum.Enum):
    executable = enum.auto()
    dynamic = enum.auto()
    object = enum.auto()

    def name_with_file_ending(self, name: str) -> str:
        if os.name == 'posix':
            if sys.platform.startswith('linux'):
                if self == Result.executable:
                    extension = 'out'
                elif self == Result.dynamic:
                    extension = 'so'
                elif self == Result.object:
                    extension = 'o'
                else:
                    raise ValueError(f'Unknown result: {self}')
            elif sys.platform == 'darwin':
                if self == Result.executable:
                    extension = 'out'
                elif self == Result.dynamic:
                    extension = 'dylib'
                elif self == Result.object:
                    extension = 'o'
                else:
                    raise ValueError(f'Unknown result: {self}')
            else:
                raise NotImplementedError(f'Unknown platform: {sys.platform}')
        elif os.name == 'nt':
            if self == Result.executable:
                extension = 'exe'
            elif self == Result.dynamic:
                extension = 'dll'
            elif self == Result.object:
                extension = 'obj'
            else:
                raise ValueError(f'Unknown result: {self}')
        else:
            raise NotImplementedError(f'Unknown os: {os.name}')

        return f'{name}.{extension}'

    def as_flag(self, compiler: str) -> str:
        if compiler in ['gcc', 'clang', 'tcc']:
            if self == Result.executable:
                return ''
            elif self == Result.dynamic:
                # `-fPIC` has no meaning on windows since all executables are
                # already position independent
                return '-shared' + ('' if os.name == 'nt' else ' -fPIC')
            elif self == Result.object:
                return '-c'
            raise NotImplementedError(f'Unknown executable type: {self}')
        elif compiler in ['cl', 'clang-cl']:
            if self == Result.executable:
                return ''
            elif self == Result.dynamic:
                # `-fPIC` has no meaning on windows since all executables are
                # already position independent
                return '/LD'
            elif self == Result.object:
                return '/c'
            raise NotImplementedError(f'Unknown executable type: {self}')
        raise NotImplementedError(f'Unknown compiler: "{compiler}"')

    def output_flag(self, compiler: str, name: str) -> str:
        if compiler in ['gcc', 'clang', 'tcc']:
            return f'-o {name}'
        elif compiler in ['cl', 'clang-cl']:
            if self == Result.executable:
                return f'/Fe{name}'
            elif self == Result.dynamic:
                return f'/Fe{name}'
            elif self == Result.object:
                return f'/Fo{name}'
            raise NotImplementedError(f'Unknown executable type: {self}')
        raise NotImplementedError(f'Unknown compiler: "{compiler}"')


@dataclasses.dataclass
class CompileCommand:
    compiler: str
    files: List[str]
    result: Result
    macros: List[Macro] = dataclasses.field(default_factory=list)
    flags: List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if temp_directory is None:
            raise RuntimeError('Temp directory has not been setup, create and assign')
        id = hash((
            self.compiler,
            tuple(sorted(self.files)),
            self.result,
            tuple(sorted([(m.name, m.value) for m in self.macros])),
            tuple(self.flags),
        ))
        self.output_name = os.path.join(temp_directory, self.result.name_with_file_ending(f'{self.compiler}_{id}'))

        src_path, _ = os.path.split(__file__)

        self.command = f'{self.compiler}'
        self.command += ' ' + ' '.join(os.path.join(src_path, f) for f in self.files)
        self.command += ' ' + self.result.as_flag(self.compiler)
        self.command += ' ' + self.result.output_flag(self.compiler, self.output_name)
        self.command += ' ' + ' '.join(m.as_flag(self.compiler) for m in self.macros)
        self.command += ' ' + ' '.join(self.flags)


class CompileError(Exception):
    pass


def compile(cc: CompileCommand) -> str:
    p = subprocess.Popen(
        cc.command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )
    out, err = p.communicate()
    if p.returncode:
        raise CompileError(
            'Could not compile command:\n'
            + '\n'
            + f'{cc.command}\n'
            + '\n'
            + ('-' * 80) + '\n'
            + f'{out}'
            + ('-' * 80) + '\n'
            + f'{err}'
            + ('-' * 80) + '\n'
        )

    return cc.output_name


def run(executable: str):
    p = subprocess.Popen(
        os.path.abspath(executable),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        text=True,
    )
    out, err = p.communicate()
    return p.returncode, out, err

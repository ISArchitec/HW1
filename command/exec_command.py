import os
import subprocess

from command.command import Command
from utils.exception import ExecutionError
from stream import InStream, OutStream
from utils.session import Session


class ExecCommand(Command):
    """Run an external program using the parent process's standard streams."""

    def __init__(self, args: list[str], in_stream: InStream, out_stream: OutStream, session: Session):
        super().__init__(args, in_stream, out_stream)
        self.session = session

    def execute(self) -> None:
        """Launch the program and map launch or exit failures to ExecutionError."""
        try:
            sub_env = os.environ.copy()
            self.session.apply(sub_env)
            result = subprocess.run(self.args, env=sub_env)
        except FileNotFoundError as error:
            raise ExecutionError(127) from error
        except OSError as error:
            raise ExecutionError(126) from error
        if result.returncode != 0:
            raise ExecutionError(result.returncode)

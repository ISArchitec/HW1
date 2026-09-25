import subprocess

from command.command import Command
from utils.exception import ExecutionError


class ExecCommand(Command):
    """Run an external program using the parent process's standard streams."""

    def execute(self) -> None:
        """Launch the program and map launch or exit failures to ExecutionError."""
        try:
            result = subprocess.run(self.args)
        except FileNotFoundError as error:
            raise ExecutionError(127) from error
        except OSError as error:
            raise ExecutionError(126) from error
        if result.returncode != 0:
            raise ExecutionError(result.returncode)

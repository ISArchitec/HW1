import subprocess

from command.command import Command
from utils.exception import ExecutionError


class ExecCommand(Command):

    def execute(self) -> None:
        try:
            result = subprocess.run(self.args)
        except FileNotFoundError as error:
            raise ExecutionError(127) from error
        except OSError as error:
            raise ExecutionError(126) from error
        if result.returncode != 0:
            raise ExecutionError(result.returncode)

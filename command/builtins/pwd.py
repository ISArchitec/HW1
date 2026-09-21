import os

from command.command import Command
from utils.exception import ExecutionError


class PwdCommand(Command):
    
    def execute(self) -> None:
        if self.args:
            raise ExecutionError(1)
        try:
            directory = os.getcwd()
        except OSError as error:
            raise ExecutionError(1) from error
        self._write(directory + "\n")

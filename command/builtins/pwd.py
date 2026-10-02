import os

from command.command import Command
from utils.exception import ExecutionError


class PwdCommand(Command):
    """Print the current working directory."""

    async def execute(self) -> None:
        """Write the working directory and reject any supplied arguments."""
        if self.args:
            raise ExecutionError(1)
        try:
            directory = os.getcwd()
        except OSError as error:
            raise ExecutionError(1) from error
        await self._write(directory + "\n")

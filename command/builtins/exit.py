from command.command import Command
from utils.exception import ExitInterrupt


class ExitCommand(Command):
    """Terminate the interpreter with a successful exit status."""

    async def _execute_unsafe(self) -> None:
        """Raise SystemExit with exit code zero."""
        raise ExitInterrupt

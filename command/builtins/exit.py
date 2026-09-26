import sys

from command.command import Command


class ExitCommand(Command):
    """Terminate the interpreter with a successful exit status."""
    
    def execute(self) -> None:
        """Raise SystemExit with exit code zero."""
        sys.exit(0)

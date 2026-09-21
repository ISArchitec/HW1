import sys

from command.command import Command


class ExitCommand(Command):
    
    def execute(self) -> None:
        sys.exit(0)

from stream import InStream, OutStream
from command.command import Command
from command.builtins import CatCommand, EchoCommand, WcCommand, PwdCommand, ExitCommand
from command.exec_command import ExecCommand


class CommandFactory:
    
    _commands: dict[str, type[Command]] = {
        "cat": CatCommand,
        "echo": EchoCommand,
        "wc": WcCommand,
        "pwd": PwdCommand,
        "exit": ExitCommand,
    }

    def create(
        self, words: list[str], in_stream: InStream, out_stream: OutStream
    ) -> Command:
        name, *args = words
        command_type = self._commands.get(name)
        if command_type is None:
            return ExecCommand(words, in_stream, out_stream)
        return command_type(args, in_stream, out_stream)

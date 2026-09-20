from abc import ABC


class CliError(Exception, ABC):
    pass


class ParserError(CliError):
    pass


class ExecutionError(CliError):
    def __init__(self, code):
        super().__init__(f"Command exited with non-zero code {code}")

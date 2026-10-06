from abc import ABC


class CliError(Exception, ABC):
    """Error, that is expected within interpreter"""
    pass


class ParserError(CliError):
    """Error, that caused by user's incorrect commands"""
    pass


class ExecutionError(CliError):
    """Error, that caused by command's failure"""
    def __init__(self, code: int):
        self.code = code
        super().__init__(f"Command exited with non-zero code {code}")

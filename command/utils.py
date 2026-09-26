from enum import Enum
from typing import TypeVar

from utils.exception import ExecutionError


Option = TypeVar("Option", bound=Enum)


def parse_options(args: list[str], option_type: type[Option]) -> tuple[set[Option], list[str]]:
    """Parse short flags and operands, honoring -- and rejecting unknown flags."""
    options: set[Option] = set()
    operands: list[str] = []
    parse_flags = True
    for arg in args:
        if parse_flags and arg == "--":
            parse_flags = False
        elif parse_flags and arg.startswith("-") and arg != "-":
            try:
                options.update(option_type(flag) for flag in arg[1:])
            except ValueError as error:
                raise ExecutionError(1) from error
        else:
            operands.append(arg)
    return options, operands

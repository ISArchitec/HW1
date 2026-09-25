from enum import Enum
from string import hexdigits, octdigits

from command.command import Command


ESCAPE_REPLACEMENTS = {
    "a": "\a",
    "b": "\b",
    "e": "\x1b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "\\": "\\",
}
OCTAL_ESCAPE_DIGITS = 3
HEX_ESCAPE_DIGITS = 2
BYTE_VALUE_COUNT = 256


class EchoOption(Enum):
    NO_NEWLINE = "n"
    ENABLE_ESCAPES = "e"
    DISABLE_ESCAPES = "E"


class EchoCommand(Command):
    def execute(self) -> None:
        options, operands = self._parse_arguments()
        text = " ".join(operands)
        stopped = False
        if EchoOption.ENABLE_ESCAPES in options:
            text, stopped = self._expand_escapes(text)
        newline = not stopped and EchoOption.NO_NEWLINE not in options
        self._write(text + ("\n" if newline else ""))

    def _parse_arguments(self) -> tuple[set[EchoOption], list[str]]:
        enabled: set[EchoOption] = set()
        index = 0
        for arg in self.args:
            if not arg.startswith("-") or len(arg) == 1:
                break
            try:
                options = [EchoOption(flag) for flag in arg[1:]]
            except ValueError:
                break
            for option in options:
                if option is EchoOption.DISABLE_ESCAPES:
                    enabled.discard(EchoOption.ENABLE_ESCAPES)
                else:
                    enabled.add(option)
            index += 1
        return enabled, self.args[index:]

    @classmethod
    def _expand_escapes(cls, text: str) -> tuple[str, bool]:
        output = []
        index = 0
        while index < len(text):
            if text[index] != "\\" or index + 1 == len(text):
                output.append(text[index])
                index += 1
                continue
            escape = text[index + 1]
            index += 2
            if escape == "c":
                return "".join(output), True
            if escape in ESCAPE_REPLACEMENTS:
                output.append(ESCAPE_REPLACEMENTS[escape])
            elif escape in {"0", "x"}:
                character, index = cls._read_numeric_escape(text, index, escape)
                output.append(character)
            else:
                output.append("\\" + escape)
        return "".join(output), False

    @staticmethod
    def _read_numeric_escape(text: str, start: int, escape: str) -> tuple[str, int]:
        if escape == "0":
            base = 8
            allowed_digits = octdigits
            max_digits = OCTAL_ESCAPE_DIGITS
            fallback = "\0"
        else:
            base = 16
            allowed_digits = hexdigits
            max_digits = HEX_ESCAPE_DIGITS
            fallback = "\\x"

        end = start
        while end < min(len(text), start + max_digits):
            if text[end] not in allowed_digits:
                break
            end += 1

        if end == start:
            return fallback, start

        value = int(text[start:end], base)

        return chr(value % BYTE_VALUE_COUNT), end

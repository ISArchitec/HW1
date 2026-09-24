import unicodedata
from enum import Enum

from command.command import Command
from command.utils import parse_options


class WcOption(Enum):
    LINES = "l"
    WORDS = "w"
    CHARACTERS = "m"
    BYTES = "c"
    MAX_LINE_LENGTH = "L"


DEFAULT_OPTIONS = {WcOption.LINES, WcOption.WORDS, WcOption.BYTES}
OUTPUT_ORDER = (
    WcOption.LINES,
    WcOption.WORDS,
    WcOption.CHARACTERS,
    WcOption.BYTES,
    WcOption.MAX_LINE_LENGTH,
)
TAB_WIDTH = 8


class WordCounter:
    def __init__(self, measure_width: bool) -> None:
        self.measure_width = measure_width
        self.counts: dict[WcOption, int] = dict.fromkeys(WcOption, 0)
        self.in_word = False
        self.width = 0

    def consume(self, chunk: str) -> None:
        self.counts[WcOption.LINES] += chunk.count("\n")
        self.counts[WcOption.CHARACTERS] += len(chunk)
        self.counts[WcOption.BYTES] += len(chunk.encode("utf-8"))
        for character in chunk:
            self._count_word(character)
            if self.measure_width:
                self._measure_character(character)

    def _count_word(self, character: str) -> None:
        if character.isspace():
            self.in_word = False
        elif not self.in_word:
            self.counts[WcOption.WORDS] += 1
            self.in_word = True

    def _measure_character(self, character: str) -> None:
        if character in "\n\r\f":
            self.finish_line()
            self.width = 0
        elif character == "\t":
            self.width += TAB_WIDTH - self.width % TAB_WIDTH
        elif character.isprintable() and not unicodedata.category(character).startswith("M"):
            self.width += 2 if unicodedata.east_asian_width(character) in {"W", "F"} else 1

    def finish_line(self) -> None:
        self.counts[WcOption.MAX_LINE_LENGTH] = max(
            self.counts[WcOption.MAX_LINE_LENGTH], self.width
        )


class WcCommand(Command):
    def execute(self) -> None:
        options, operands = parse_options(self.args, WcOption)
        options = options or DEFAULT_OPTIONS
        order = [option for option in OUTPUT_ORDER if option in options]
        paths = self._input_paths(operands)
        totals = dict.fromkeys(WcOption, 0)
        for path in paths:
            counts = self._count_input(path, WcOption.MAX_LINE_LENGTH in options)
            self._accumulate(totals, counts)
            self._write_counts([counts[option] for option in order], path)
        if len(paths) > 1:
            self._write_counts([totals[option] for option in order], "total")

    def _count_input(self, path: str | None, measure_width: bool) -> dict[WcOption, int]:
        counter = WordCounter(measure_width)
        for chunk in self._read_chunks(path):
            counter.consume(chunk)
        counter.finish_line()
        return counter.counts

    @staticmethod
    def _accumulate(totals: dict[WcOption, int], counts: dict[WcOption, int]) -> None:
        for option, count in counts.items():
            if option is WcOption.MAX_LINE_LENGTH:
                totals[option] = max(totals[option], count)
            else:
                totals[option] += count

    def _write_counts(self, counts: list[int], label: str | None) -> None:
        suffix = f" {label}" if label is not None else ""
        self._write(" ".join(map(str, counts)) + suffix + "\n")

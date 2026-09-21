import unicodedata

from command.command import Command
from command.utils import parse_options


class WcCommand(Command):
    
    def execute(self) -> None:
        options, files = parse_options(self.args, set("lwcmL"))
        if not options:
            options = set("lwc")
        order = [flag for flag in "lwmcL" if flag in options]
        totals = dict.fromkeys("lwmcL", 0)
        paths: list[str | None] = list(files) if files else [None]
        for path in paths:
            counts = dict.fromkeys("lwmcL", 0)
            in_word = False
            width = 0
            for chunk in self._read_chunks(path):
                counts["l"] += chunk.count("\n")
                counts["m"] += len(chunk)
                counts["c"] += len(chunk.encode("utf-8"))
                for character in chunk:
                    if character.isspace():
                        in_word = False
                    elif not in_word:
                        counts["w"] += 1
                        in_word = True
                    if "L" in options:
                        if character in "\n\r\f":
                            counts["L"] = max(counts["L"], width)
                            width = 0
                        elif character == "\t":
                            width += 8 - width % 8
                        elif character.isprintable() and not unicodedata.category(character).startswith("M"):
                            width += 2 if unicodedata.east_asian_width(character) in {"W", "F"} else 1
            counts["L"] = max(counts["L"], width)
            for flag in "lwmc":
                totals[flag] += counts[flag]
            totals["L"] = max(totals["L"], counts["L"])
            self._write_counts([counts[flag] for flag in order], path)
        if len(paths) > 1:
            self._write_counts([totals[flag] for flag in order], "total")

    def _write_counts(self, counts: list[int], label: str | None) -> None:
        suffix = f" {label}" if label is not None else ""
        self._write(" ".join(map(str, counts)) + suffix + "\n")

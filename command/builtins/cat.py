from command.command import Command
from command.utils import parse_options


class CatCommand(Command):
    
    def execute(self) -> None:
        options, files = parse_options(self.args, set("nbsETvA"))
        if "A" in options:
            options.update("vET")
        paths: list[str | None] = list(files) if files else [None]
        line_number = 1
        line_start = True
        previous_blank = False
        for path in paths:
            for chunk in self._read_chunks(path):
                if not options:
                    self._write(chunk)
                    continue
                output = []
                for character in chunk:
                    blank = line_start and character == "\n"
                    if "s" in options and blank and previous_blank:
                        continue
                    if line_start:
                        if ("b" in options and not blank) or (
                            "n" in options and "b" not in options
                        ):
                            output.append(f"{line_number:6}\t")
                            line_number += 1
                    if character == "\n":
                        output.append("$\n" if "E" in options else "\n")
                        previous_blank = blank
                        line_start = True
                    else:
                        output.append(self._display(character, options))
                        line_start = False
                self._write("".join(output))

    @staticmethod
    def _display(character: str, options: set[str]) -> str:
        if character == "\t":
            return "^I" if "T" in options else character
        if "v" not in options:
            return character
        output = []
        for byte in character.encode("utf-8"):
            if byte >= 128:
                output.append("M-")
                byte -= 128
            if byte < 32:
                output.append("^" + chr(byte + 64))
            elif byte == 127:
                output.append("^?")
            else:
                output.append(chr(byte))
        return "".join(output)

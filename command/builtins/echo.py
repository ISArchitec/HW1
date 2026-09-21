from command.command import Command


class EchoCommand(Command):
    
    def execute(self) -> None:
        newline = True
        escapes = False
        index = 0
        for arg in self.args:
            if not arg.startswith("-") or len(arg) == 1 or not set(arg[1:]) <= set("neE"):
                break
            for flag in arg[1:]:
                if flag == "n":
                    newline = False
                else:
                    escapes = flag == "e"
            index += 1
        text = " ".join(self.args[index:])
        if escapes:
            text, stopped = self._expand_escapes(text)
            if stopped:
                newline = False
        self._write(text + ("\n" if newline else ""))

    @staticmethod
    def _expand_escapes(text: str) -> tuple[str, bool]:
        replacements = {
            "a": "\a", "b": "\b", "e": "\x1b", "f": "\f",
            "n": "\n", "r": "\r", "t": "\t", "v": "\v", "\\": "\\",
        }
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
            if escape in replacements:
                output.append(replacements[escape])
            elif escape in {"0", "x"}:
                digits = "01234567" if escape == "0" else "0123456789abcdefABCDEF"
                limit = 3 if escape == "0" else 2
                start = index
                while index < len(text) and index - start < limit and text[index] in digits:
                    index += 1
                if index > start:
                    value = int(text[start:index], 8 if escape == "0" else 16)
                    output.append(chr(value % 256))
                else:
                    output.append("\0" if escape == "0" else "\\x")
            else:
                output.append("\\" + escape)
        return "".join(output), False

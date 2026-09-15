from stream import InStream, OutStream, Console


class GlobalConsole:
    stdin: InStream
    stdout: OutStream
    stderr: OutStream

    def __init__(self):
        self.stdin = Console()
        self.stdout = Console()
        self.stderr = Console()

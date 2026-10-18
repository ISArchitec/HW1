from stream import Console, InStream, OutStream


class GlobalConsole:
    """Represents console for interpreter, in which it interacts with user"""

    stdin: InStream
    stdout: OutStream
    stderr: OutStream

    def __init__(self):
        self.stdin = Console()
        self.stdout = Console()
        self.stderr = Console()

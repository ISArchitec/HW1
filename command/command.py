from abc import ABC, abstractmethod
from collections.abc import Iterator

from stream import InStream, OutStream
from utils.exception import ExecutionError


CHUNK_SIZE = 8192


class Command(ABC):
    """Define the command interface and shared stream and file helpers."""
    
    def __init__(self, args: list[str], in_stream: InStream, out_stream: OutStream):
        """Copy command arguments and store the input and output streams."""
        self.args = args.copy()
        self.in_stream = in_stream
        self.out_stream = out_stream

    def _read_chunks(self, path: str | None = None) -> Iterator[str]:
        try:
            if path is None:
                yield from iter(self.in_stream.read_line, "")
            else:
                with open(path, encoding="utf-8", newline="") as source:
                    yield from iter(lambda: source.read(CHUNK_SIZE), "")
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    @staticmethod
    def _input_paths(operands: list[str]) -> list[str | None]:
        return list(operands) if operands else [None]

    def _write(self, text: str) -> None:
        try:
            self.out_stream.write(text)
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    @abstractmethod
    def execute(self) -> None:
        """Run the command, raising ExecutionError on an execution failure."""
        pass

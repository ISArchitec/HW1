from abc import ABC, abstractmethod
from collections.abc import Iterator

from stream import InStream, OutStream
from utils.exception import ExecutionError


class Command(ABC):
    
    def __init__(self, args: list[str], in_stream: InStream, out_stream: OutStream):
        self.args = args.copy()
        self.in_stream = in_stream
        self.out_stream = out_stream

    def _read_chunks(self, path: str | None = None) -> Iterator[str]:
        try:
            if path is None:
                yield from iter(self.in_stream.read_line, "")
            else:
                with open(path, encoding="utf-8", newline="") as source:
                    yield from iter(lambda: source.read(8192), "")
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    def _write(self, text: str) -> None:
        try:
            self.out_stream.write(text)
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    @abstractmethod
    def execute(self) -> None:
        pass

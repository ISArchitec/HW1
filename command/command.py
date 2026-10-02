from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

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

    async def _read_chunks(self, path: str | None = None) -> AsyncIterator[str]:
        try:
            if path is None:
                line = await self.in_stream.read_line()
                while line:
                    yield line
                    line = await self.in_stream.read_line()
            else:
                # TODO think about async file operations
                with open(path, encoding="utf-8", newline="") as source:
                    chunk = source.read(CHUNK_SIZE)
                    while chunk:
                        yield chunk
                        chunk = source.read(CHUNK_SIZE)
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    @staticmethod
    def _input_paths(operands: list[str]) -> list[str | None]:
        return list(operands) if operands else [None]

    async def _write(self, text: str) -> None:
        try:
            await self.out_stream.write(text)
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error

    @abstractmethod
    async def execute(self) -> None:
        """Run the command, raising ExecutionError on an execution failure."""
        pass

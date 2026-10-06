import asyncio

from stream import InStream, OutStream


class Pipe(InStream, OutStream):
    """Stream, that represents shared memory between commands through pipe"""

    def __init__(self, size: int):
        super().__init__()
        self.lines = asyncio.Queue(maxsize=size)
        self.current_line = ""
        self.current_line_index = 0

    async def read_char(self) -> str:
        if self.current_line_index >= len(self.current_line):
            if self.is_closed_from_writer() and self.lines.empty():
                # If we are closed, and queue is empty, we already read EOF, no race condition should be here
                return ""
            self.current_line_index = 0
            self.current_line = await self.lines.get()
        index = self.current_line_index
        self.current_line_index += 1
        return self.current_line[index]

    async def read_line(self) -> str:
        index = self.current_line_index
        self.current_line_index = 0
        if index >= len(self.current_line):
            if self.is_closed_from_writer() and self.lines.empty():
                # If we are closed, and queue is empty, we already read EOF, no race condition should be here
                return ""
            return await self.lines.get()
        return self.current_line[index:]

    async def write(self, string: str) -> None:
        if self.is_closed_from_reader():
            return
        await self.lines.put(string)

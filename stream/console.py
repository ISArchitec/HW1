import aioconsole

from stream.in_stream import InStream
from stream.out_stream import OutStream


class Console(InStream, OutStream):
    """Stream, that represents basic input/output to terminal"""

    def __init__(self):
        super().__init__()
        self.buffer = ""
        self.buffer_index = 0

    async def read_char(self) -> str:
        if self.buffer_index >= len(self.buffer):
            if self.is_closed_from_writer():
                return ""
            self.buffer = await aioconsole.ainput()
            self.buffer_index = 0
        index = self.buffer_index
        self.buffer_index += 1
        return self.buffer[index]

    async def read_line(self) -> str:
        index = self.buffer_index
        self.buffer_index = 0
        if index >= len(self.buffer):
            if self.is_closed_from_writer():
                return ""
            return await aioconsole.ainput()
        return self.buffer[index:]

    async def write(self, string: str) -> None:
        if self.is_closed_from_reader():
            return
        await aioconsole.aprint(string, end="")

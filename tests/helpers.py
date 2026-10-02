import io

from stream import InStream, OutStream


class MemoryStream(InStream, OutStream):
    def __init__(self, text=""):
        self.buffer = io.StringIO(text)

    async def read_char(self):
        return self.buffer.read(1)

    async def read_line(self):
        return self.buffer.readline()

    async def write(self, string):
        self.buffer.write(string)

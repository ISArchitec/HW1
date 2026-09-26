import io

from stream import InStream, OutStream


class MemoryStream(InStream, OutStream):
    def __init__(self, text=""):
        self.buffer = io.StringIO(text)

    def read_char(self):
        return self.buffer.read(1)

    def read_line(self):
        return self.buffer.readline()

    def write(self, string):
        self.buffer.write(string)

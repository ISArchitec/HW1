from stream import InStream, OutStream


class Console(InStream, OutStream):
    def __init__(self):
        self.buffer = str()
        self.buffer_index = 0

    def read_char(self) -> str:
        if self.buffer_index >= len(self.buffer):
            self.buffer = input()
            self.buffer_index = 0
        index = self.buffer_index
        self.buffer_index += 1
        return self.buffer[index]

    def read_line(self) -> str:
        index = self.buffer_index
        self.buffer_index = 0
        if index >= len(self.buffer):
            return input()
        return self.buffer[index:]

    def write(self, string: str) -> None:
        print(string, end='')

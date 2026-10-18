from abc import ABC, abstractmethod


class InStream(ABC):
    """Interface for stream, from which we can read"""

    def __init__(self):
        self._closed = False

    @abstractmethod
    async def read_char(self) -> str:
        """Read only one symbol"""
        pass

    @abstractmethod
    async def read_line(self) -> str:
        """Read symbols until the end of the line"""
        pass

    async def close_from_reader(self):
        """Signal that we are stop reading from stream"""
        self._closed = True

    def is_closed_from_reader(self):
        """Returns if stream stopped for reading"""
        return self._closed

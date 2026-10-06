from abc import ABC, abstractmethod


class OutStream(ABC):
    """Interface for stream, to which we can write"""

    def __init__(self):
        self._closed = False

    @abstractmethod
    async def write(self, string: str) -> None:
        """Write any string to stream"""
        pass

    async def close_from_writer(self):
        """Signal that we are stop reading from stream"""
        await self.write("")
        self._closed = True

    def is_closed_from_writer(self):
        """Returns if stream stopped for reading"""
        return self._closed

from abc import ABC, abstractmethod


class OutStream(ABC):
    """Interface for stream, to which we can write"""

    @abstractmethod
    def write(self, string: str) -> None:
        """Write any string to stream"""
        pass

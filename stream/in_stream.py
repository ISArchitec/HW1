from abc import ABC, abstractmethod


class InStream(ABC):
    """Interface for stream, from which we can read"""

    @abstractmethod
    def read_char(self) -> str:
        """Read only one symbol"""
        pass

    @abstractmethod
    def read_line(self) -> str:
        """Read symbols until the end of the line"""
        pass

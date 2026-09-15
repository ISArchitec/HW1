from abc import ABC, abstractmethod


class InStream(ABC):
    @abstractmethod
    def read_char(self) -> str:
        pass

    @abstractmethod
    def read_line(self) -> str:
        pass

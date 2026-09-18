from abc import ABC, abstractmethod


class OutStream(ABC):
    @abstractmethod
    def write(self, string: str) -> None:
        pass

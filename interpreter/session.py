from typing import Self

class Session:
    def get(self: Self, key: str) -> str:
        raise NotImplementedError()

    def set(self: Self, key: str, value:  str):
        raise NotImplementedError()

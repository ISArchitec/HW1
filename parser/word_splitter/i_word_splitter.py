from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class IWordSplitter(ABC):
    """Everything a word state is allowed to do with the splitter"""

    @abstractmethod
    def add_word(self, symbol: str = "") -> None:
        """Start a new word, optionally with its first symbol"""

    @abstractmethod
    def append(self, symbol: str) -> None:
        """Append symbol to the current word"""

    @abstractmethod
    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        """Replace current state with the one built from its class"""

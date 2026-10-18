from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class IPipeSplitter(ABC):
    """Everything a pipe state is allowed to do with the splitter"""

    @abstractmethod
    def append(self, symbol: str) -> None:
        """Append symbol to the sentence being built"""

    @abstractmethod
    def get_ignore_quote(self) -> bool:
        """Return whether we should ignore the quote"""

    @abstractmethod
    def add_sentence(self) -> None:
        """Start a new sentence"""

    @abstractmethod
    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        """Replace current state with the one built from its class"""

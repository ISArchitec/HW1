from abc import ABC, abstractmethod
from typing import Any, Callable


class IPipeSplitter(ABC):
    """Everything a pipe state is allowed to do with the splitter"""

    @abstractmethod
    def append(self, symbol: str) -> None:
        """Append symbol to the sentence being built"""

    @abstractmethod
    def add_sentence(self) -> None:
        """Start a new sentence"""

    @abstractmethod
    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        """Replace current state with the one built from its class"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class ISubstitutor(ABC):
    """Everything a substitution state is allowed to do with the substitutor"""

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Feed symbol to the automaton"""

    @abstractmethod
    def add_text(self, text: str) -> None:
        """Append text to the result"""

    @abstractmethod
    def add_with_quote_and_dollar_tracking(self, symbol: str) -> None:
        """Append symbol to the result, tracking quotes in it"""

    @abstractmethod
    def get_variable(self, name: str) -> str:
        """Read session variable by name"""

    @abstractmethod
    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        """Replace current state with the one built from its class"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.substitution.substitutor import Substitutor


class SubstitutionState(ABC):
    """Base state of variable substitution"""

    def __init__(self, substitutor: Substitutor):
        self._substitutor = substitutor

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

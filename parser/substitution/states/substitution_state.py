from abc import ABC, abstractmethod

from parser.substitution.i_substitutor import ISubstitutor


class SubstitutionState(ABC):
    """Base state of variable substitution"""

    def __init__(self, substitutor: ISubstitutor):
        self._substitutor = substitutor

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

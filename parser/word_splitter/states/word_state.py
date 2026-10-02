from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.word_splitter.word_splitter import WordSplitter


class WordState(ABC):
    """Base state of splitting sentence into words"""

    def __init__(self, splitter: WordSplitter):
        self._splitter = splitter

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

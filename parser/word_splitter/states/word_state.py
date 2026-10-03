from abc import ABC, abstractmethod

from parser.word_splitter.i_word_splitter import IWordSplitter


class WordState(ABC):
    """Base state of splitting sentence into words"""

    def __init__(self, splitter: IWordSplitter):
        self._splitter = splitter

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

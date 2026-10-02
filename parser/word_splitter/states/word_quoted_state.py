from __future__ import annotations

from typing import TYPE_CHECKING

from parser.word_splitter.states.word_state import WordState
from utils.exception import ParserError

if TYPE_CHECKING:
    from parser.word_splitter.word_splitter import WordSplitter


class WordQuotedState(WordState):
    """State of reading quoted word, quote symbol is kept in state"""

    def __init__(self, splitter: WordSplitter, quote: str):
        super().__init__(splitter)
        self.__quote = quote

    def add_symbol(self, symbol: str) -> None:
        from parser.word_splitter.states.word_unquoted_state import WordUnquotedState

        if symbol == self.__quote:
            self._splitter.set_state(WordUnquotedState)
        else:
            self._splitter.append_to_word(symbol)

    def finish(self) -> None:
        raise ParserError("Unclosed quote")

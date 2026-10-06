from collections.abc import Callable, Iterator
from typing import Any

from parser.word_splitter.i_word_splitter import IWordSplitter
from parser.word_splitter.states.word_skip_state import WordSkipState
from parser.word_splitter.states.word_state import WordState
from utils.exception import ParserError


class WordSplitter(IWordSplitter):
    """Container, that splits sentence into words by whitespaces and quotes.
    Feed symbols via add_symbol, read result via __iter__ (finish is called automatically)
    """

    def __init__(self):
        self.__words: list[str] = []
        self.__state: WordState = WordSkipState(self)
        self.__ignore_quote: bool = False

    def add_symbol(self, symbol: str) -> None:
        "Consumes 1 symbol"
        if self.__ignore_quote:
            self.__ignore_quote = False
            if symbol in {"\\", "'", '"'}:
                self.__state.add_escaped_symbol(symbol)
            else:
                self.__state.add_symbol("\\")
                self.__state.add_symbol(symbol)
            return
        if symbol == "\\":
            self.__ignore_quote = True
            return
        self.__state.add_symbol(symbol)

    def get_ignore_quote(self) -> bool:
        "Returns True if previous symbol is a backslash"
        return self.__ignore_quote

    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        "Sets splitter state"
        self.__state = state_class(self, *args)

    def add_word(self, symbol: str = "") -> None:
        "Adds new word"
        self.__words.append(symbol)

    def append(self, symbol: str) -> None:
        "Appends symbol to the last word"
        self.__words[-1] += symbol

    def __iter__(self) -> Iterator[str]:
        if self.__ignore_quote:
            self.__ignore_quote = False
            self.__state.add_escaped_symbol("\\")
        self.__state.finish()
        if len(self.__words) == 0:
            raise ParserError("Sentence couldn't be empty")
        return iter(self.__words)

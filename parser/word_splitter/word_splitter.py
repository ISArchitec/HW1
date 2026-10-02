from collections.abc import Iterator

from parser.word_splitter.states.word_skip_state import WordSkipState
from parser.word_splitter.states.word_state import WordState
from utils.exception import ParserError


class WordSplitter:
    """Container, that splits sentence into words by whitespaces and quotes.
    Feed symbols via add_symbol, read result via __iter__ (finish is called automatically)
    """

    def __init__(self):
        self.__words: list[str] = []
        self.__state: WordState = WordSkipState(self)
        self.__finished = False

    def add_symbol(self, symbol: str) -> None:
        self.__state.add_symbol(symbol)

    def set_state(self, state_class, *args) -> None:
        self.__state = state_class(self, *args)

    def finish(self) -> None:
        if not self.__finished:
            self.__state.finish()
            self.__finished = True
            if len(self.__words) == 0:
                raise ParserError("Sentence couldn't be empty")

    def start_word(self, symbol: str = "") -> None:
        self.__words.append(symbol)

    def append_to_word(self, symbol: str) -> None:
        self.__words[-1] += symbol

    def __iter__(self) -> Iterator[str]:
        if not self.__finished:
            self.finish()
        return iter(self.__words)

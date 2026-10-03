from parser.word_splitter.i_word_splitter import IWordSplitter
from parser.word_splitter.states.word_state import WordState
from utils.exception import ParserError


class WordQuotedState(WordState):
    """State of reading quoted word, quote symbol is kept in state"""

    def __init__(self, splitter: IWordSplitter, quote: str):
        super().__init__(splitter)
        self.__quote = quote

    def add_symbol(self, symbol: str) -> None:
        from parser.word_splitter.states.word_unquoted_state import WordUnquotedState

        if symbol == self.__quote:
            self._splitter.set_state(WordUnquotedState)
        else:
            self._splitter.append(symbol)

    def finish(self) -> None:
        raise ParserError("Unclosed quote")

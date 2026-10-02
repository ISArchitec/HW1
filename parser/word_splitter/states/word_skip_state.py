from parser.word_splitter.states.word_state import WordState


class WordSkipState(WordState):
    """State of skipping whitespaces between words"""

    def add_symbol(self, symbol: str) -> None:
        from parser.word_splitter.states.word_quoted_state import WordQuotedState
        from parser.word_splitter.states.word_unquoted_state import WordUnquotedState
        if symbol == "'":
            self._splitter.start_word()
            self._splitter.set_state(WordQuotedState, "'")
        elif symbol == '"':
            self._splitter.start_word()
            self._splitter.set_state(WordQuotedState, '"')
        elif not symbol.isspace():
            self._splitter.start_word(symbol)
            self._splitter.set_state(WordUnquotedState)
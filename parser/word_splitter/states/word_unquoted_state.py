from parser.word_splitter.states.word_state import WordState


class WordUnquotedState(WordState):
    """State of reading unquoted word"""

    def add_symbol(self, symbol: str) -> None:
        from parser.word_splitter.states.word_quoted_state import WordQuotedState
        from parser.word_splitter.states.word_skip_state import WordSkipState

        if symbol.isspace():
            self._splitter.set_state(WordSkipState)
        elif symbol == "'":
            self._splitter.set_state(WordQuotedState, "'")
        elif symbol == '"':
            self._splitter.set_state(WordQuotedState, '"')
        else:
            self._splitter.append_to_word(symbol)

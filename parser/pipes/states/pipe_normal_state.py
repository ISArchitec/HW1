from parser.pipes.states.pipe_state import PipeState

class PipeNormalState(PipeState):
    """State of ordinary symbols, '|' starts new sequence"""

    def add_symbol(self, symbol: str) -> None:
        from parser.pipes.states.pipe_quoted_state import PipeQuotedState
        if symbol == "|":
            self._splitter.add_sentence()
            return
        self._splitter.append(symbol)
        if symbol == "'":
            self._splitter.set_state(PipeQuotedState, "'")
        elif symbol == '"':
            self._splitter.set_state(PipeQuotedState, '"')

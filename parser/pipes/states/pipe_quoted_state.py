from parser.pipes.i_pipe_splitter import IPipeSplitter
from parser.pipes.states.pipe_state import PipeState


class PipeQuotedState(PipeState):
    """State inside quotes, '|' is an ordinary symbol here.
    The quote symbol is an additional field of the state
    """

    def __init__(self, splitter: IPipeSplitter, quote: str):
        super().__init__(splitter)
        self.__quote = quote

    def add_symbol(self, symbol: str) -> None:
        from parser.pipes.states.pipe_normal_state import PipeNormalState

        self._splitter.append(symbol)
        if symbol == self.__quote:
            self._splitter.set_state(PipeNormalState)

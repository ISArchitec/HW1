from collections.abc import Iterator

from parser.pipes.states.pipe_state import PipeState
from parser.pipes.states.pipe_normal_state import PipeNormalState

class PipeSplitter:
    """Container, that splits input into sequences by '|' outside quotes.
    Feed symbols via add_symbol, read result via __iter__
    """

    def __init__(self):
        self.__sequences: list[str] = [""]
        self.__state: PipeState = PipeNormalState(self)

    def add_symbol(self, symbol: str) -> None:
        "consumes 1 symbol"
        self.__state.add_symbol(symbol)

    def set_state(self, state_class, *args) -> None:
        "sets splitter state"
        self.__state = state_class(self, *args)

    def append(self, symbol: str) -> None:
        "append symbol to last word"
        self.__sequences[-1] += symbol

    def add_word(self) -> None:
        "adds new word"
        self.__sequences.append("")

    def __iter__(self) -> Iterator[str]:
        self.__state.finish()
        return iter(self.__sequences)

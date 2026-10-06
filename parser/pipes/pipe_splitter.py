from collections.abc import Callable, Iterator
from typing import Any

from parser.pipes.i_pipe_splitter import IPipeSplitter
from parser.pipes.states.pipe_normal_state import PipeNormalState
from parser.pipes.states.pipe_state import PipeState


class PipeSplitter(IPipeSplitter):
    """Container, that splits input into sequences by '|' outside quotes.
    Feed symbols via add_symbol, read result via __iter__
    """

    def __init__(self):
        self.__sequences: list[str] = [""]
        self.__state: PipeState = PipeNormalState(self)
        self.__ignore_quote: bool = False

    def add_symbol(self, symbol: str) -> None:
        "Consumes 1 symbol"
        self.__state.add_symbol(symbol)
        if not self.__ignore_quote and symbol == '\\':
            self.__ignore_quote = True
        else:
            self.__ignore_quote = False

    def get_ignore_quote(self) -> bool:
        "Returns True if previous symbol is \\"
        return self.__ignore_quote

    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        "Sets splitter state"
        self.__state = state_class(self, *args)

    def append(self, symbol: str) -> None:
        "Appends symbol to the last sentence"
        self.__sequences[-1] += symbol

    def add_sentence(self) -> None:
        "Adds new sentence"
        self.__sequences.append("")

    def __iter__(self) -> Iterator[str]:
        self.__state.finish()
        return iter(self.__sequences)

from abc import ABC, abstractmethod

from parser.pipes.i_pipe_splitter import IPipeSplitter


class PipeState(ABC):
    """Base state of pipe recognition"""

    def __init__(self, splitter: IPipeSplitter):
        self._splitter = splitter

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

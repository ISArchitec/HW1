from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.pipes.pipe_splitter import PipeSplitter


class PipeState(ABC):
    """Base state of pipe recognition"""

    def __init__(self, splitter: PipeSplitter):
        self._splitter = splitter

    @abstractmethod
    def add_symbol(self, symbol: str) -> None:
        """Process one symbol of input"""

    def finish(self) -> None:
        """Process end of input"""
        return None

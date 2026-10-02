from __future__ import annotations

from typing import TYPE_CHECKING

from parser.substitution.states.substitution_state import SubstitutionState
from parser.utils.utils import is_token_symbol

if TYPE_CHECKING:
    from parser.substitution.substitutor import Substitutor


class SubstitutionTokenState(SubstitutionState):
    """State of reading variable name outside braces,
    keeps already read part in token
    """

    def __init__(self, substitutor: Substitutor, token: str):
        super().__init__(substitutor)
        self.__token = token

    def add_symbol(self, symbol: str) -> None:
        if is_token_symbol(symbol, len(self.__token)):
            self.__token += symbol
        else:
            self._substitutor.add_text(self._substitutor.get_variable(self.__token))
            self._substitutor.add_with_quote_tracking(symbol)

    def finish(self) -> None:
        self._substitutor.add_text(self._substitutor.get_variable(self.__token))

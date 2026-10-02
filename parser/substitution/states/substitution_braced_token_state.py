from __future__ import annotations

from typing import TYPE_CHECKING

from parser.substitution.states.substitution_state import SubstitutionState
from parser.utils.utils import is_token_symbol
from utils.exception import ParserError

if TYPE_CHECKING:
    from parser.substitution.substitutor import Substitutor


class SubstitutionBracedTokenState(SubstitutionState):
    """State of reading variable name in braces: ${name}"""

    def __init__(self, substitutor: Substitutor):
        super().__init__(substitutor)
        self.__token = ""

    def add_symbol(self, symbol: str) -> None:
        from parser.substitution.states.substitution_normal_state import SubstitutionNormalState

        if is_token_symbol(symbol, len(self.__token)):
            self.__token += symbol
        elif symbol == "}":
            if len(self.__token) == 0:
                raise ParserError("wrong substitution")
            self._substitutor.add_text(self._substitutor.get_variable(self.__token))
            self._substitutor.set_state(SubstitutionNormalState)
        else:
            raise ParserError("unclosed brace")

    def finish(self) -> None:
        raise ParserError("unclosed brace")

from collections.abc import Callable
from typing import Any

from parser.substitution.i_substitutor import ISubstitutor
from parser.substitution.states.substitution_normal_state import SubstitutionNormalState
from parser.substitution.states.substitution_post_dollar_state import SubstitutionPostDollarState
from parser.substitution.states.substitution_single_quoted_state import (
    SubstitutionSingleQuotedState,
)
from parser.substitution.states.substitution_state import SubstitutionState
from utils.session import Session


class Substitutor(ISubstitutor):
    """Container, that substitutes variables from session into sentence.
    Feed symbols via add_symbol, read result via __str__
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__result = ""
        self.__in_double_quotes = False
        self.__state: SubstitutionState = SubstitutionNormalState(self)

    def add_symbol(self, symbol: str) -> None:
        "Consumes symbol"
        self.__state.add_symbol(symbol)

    def set_state(self, state_class: Callable[..., Any], *args: Any) -> None:
        "Sets state"
        self.__state = state_class(self, *args)

    def add_text(self, text: str) -> None:
        "Adds text to result"
        self.__result += text

    def add_with_quote_and_dollar_tracking(self, symbol: str) -> None:
        """Append symbol tracking quotes in it"""
        if symbol == "$":
            self.set_state(SubstitutionPostDollarState)
            return
        self.__result += symbol
        if symbol == "'" and not self.__in_double_quotes:
            self.set_state(SubstitutionSingleQuotedState)
        else:
            if symbol == '"':
                self.__in_double_quotes = not self.__in_double_quotes
            self.set_state(SubstitutionNormalState)

    def get_variable(self, name: str) -> str:
        "Gets session variable"
        return (
            self.__session.get(name).replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
        )

    def __str__(self) -> str:
        self.__state.finish()
        return self.__result

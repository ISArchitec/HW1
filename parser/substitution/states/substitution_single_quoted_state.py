from parser.substitution.i_substitutor import ISubstitutor
from parser.substitution.states.substitution_normal_state import SubstitutionNormalState
from parser.substitution.states.substitution_state import SubstitutionState


class SubstitutionSingleQuotedState(SubstitutionState):
    """State inside '...': symbols are appended without substitution"""

    def __init__(self, substitutor: ISubstitutor):
        super().__init__(substitutor)
        self.__is_escaped = False

    def add_symbol(self, symbol: str) -> None:
        self._substitutor.add_text(symbol)
        if symbol == "'" and not self.__is_escaped:
            self._substitutor.set_state(SubstitutionNormalState)
        if symbol == "\\" and not self.__is_escaped:
            self.__is_escaped = True
        else:
            self.__is_escaped = False

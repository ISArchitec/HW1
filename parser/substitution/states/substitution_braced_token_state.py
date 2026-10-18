from parser.substitution.i_substitutor import ISubstitutor
from parser.substitution.states.substitution_normal_state import SubstitutionNormalState
from parser.substitution.states.substitution_state import SubstitutionState
from parser.utils.utils import is_token_symbol
from utils.exception import ParserError


class SubstitutionBracedTokenState(SubstitutionState):
    """State of reading variable name in braces: ${name}"""

    def __init__(self, substitutor: ISubstitutor):
        super().__init__(substitutor)
        self.__token = ""

    def add_symbol(self, symbol: str) -> None:
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

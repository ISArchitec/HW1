from utils.session import Session
from parser.substitution.states.substitution_state import SubstitutionState
from parser.substitution.states.substitution_normal_state import SubstitutionNormalState
from parser.substitution.states.substitution_single_quoted_state import SubstitutionSingleQuotedState

class Substitutor:
    """Container, that substitutes variables from session into sentence.
    Feed symbols via add_symbol, read result via __str__ (finish is called automatically)
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__result = ""
        self.__in_double_quotes = False
        self.__state: SubstitutionState = SubstitutionNormalState(self)

    def add_symbol(self, symbol: str) -> None:
        "Consumes symbol"
        self.__state.add_symbol(symbol)

    def set_state(self, state_class, *args) -> None:
        "Sets state"
        self.__state = state_class(self, *args)

    def add_text(self, text: str) -> None:
        "Adds text to result"
        self.__result += text

    def add_with_quote_tracking(self, symbol: str) -> None:
        """Append symbol tracking quotes in it"""
        self.__result += symbol
        if symbol == "'" and not self.__in_double_quotes:
            self.set_state(SubstitutionSingleQuotedState)
        else:
            if symbol == '"':
                self.__in_double_quotes = not self.__in_double_quotes
            self.set_state(SubstitutionNormalState)

    def get_variable(self, name: str) -> str:
        "Gets session variable"
        return self.__session.get(name)

    def __str__(self) -> str:
        self.__state.finish()
        return self.__result

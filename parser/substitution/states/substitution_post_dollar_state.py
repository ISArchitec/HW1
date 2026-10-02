from parser.substitution.states.substitution_state import SubstitutionState
from parser.utils.utils import is_token_symbol

class SubstitutionPostDollarState(SubstitutionState):
    """State after '$': token symbol, '{' or ordinary symbol is expected"""

    def add_symbol(self, symbol: str) -> None:
        from parser.substitution.states.substitution_token_state import SubstitutionTokenState
        from parser.substitution.states.substitution_braced_token_state import  SubstitutionBracedTokenState
        if is_token_symbol(symbol, 0):
            self._substitutor.set_state(SubstitutionTokenState, symbol)
        elif symbol == "{":
            self._substitutor.set_state(SubstitutionBracedTokenState)
        else:
            self._substitutor.add_symbol("$")
            self._substitutor.add_with_quote_tracking(symbol)

    def finish(self) -> None:
        self._substitutor.add_text("$")

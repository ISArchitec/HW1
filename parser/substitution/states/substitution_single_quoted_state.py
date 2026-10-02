from parser.substitution.states.substitution_normal_state import SubstitutionNormalState
from parser.substitution.states.substitution_state import SubstitutionState


class SubstitutionSingleQuotedState(SubstitutionState):
    """State inside '...': symbols are appended without substitution"""

    def add_symbol(self, symbol: str) -> None:
        self._substitutor.add_text(symbol)
        if symbol == "'":
            self._substitutor.set_state(SubstitutionNormalState)

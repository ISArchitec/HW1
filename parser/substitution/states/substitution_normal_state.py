from parser.substitution.states.substitution_state import SubstitutionState


class SubstitutionNormalState(SubstitutionState):
    """State of ordinary symbols outside quotes"""

    def add_symbol(self, symbol: str) -> None:
        from parser.substitution.states.substitution_escaped_state import SubstitutionEscapedState
        from parser.substitution.states.substitution_post_dollar_state import (
            SubstitutionPostDollarState,
        )
        
        if symbol == "\\":
            self._substitutor.set_state(SubstitutionEscapedState)
        else:
            self._substitutor.add_with_quote_and_dollar_tracking(symbol)

from parser.substitution.states.substitution_state import SubstitutionState


class SubstitutionEscapedState(SubstitutionState):
    """State after '\\': '$' and '\\' lose their special meaning"""

    def add_symbol(self, symbol: str) -> None:
        if symbol not in ("$", "\\"):
            self._substitutor.add_text("\\")
        self._substitutor.add_with_quote_tracking(symbol)

    def finish(self) -> None:
        self._substitutor.add_text("\\")

from parser.substitution.states.substitution_state import SubstitutionState


class SubstitutionEscapedState(SubstitutionState):
    """State after '\\': '$' and '\\' lose their special meaning"""

    def add_symbol(self, symbol: str) -> None:
        from parser.substitution.states.substitution_normal_state import SubstitutionNormalState

        if symbol != "$":
            self._substitutor.add_text("\\")
        self._substitutor.add_text(symbol)
        self._substitutor.set_state(SubstitutionNormalState)

    def finish(self) -> None:
        self._substitutor.add_text("\\")

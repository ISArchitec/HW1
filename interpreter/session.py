class Session:
    """Storage for environmental variables and other session-specific parameters"""

    def get(self, key: str) -> str:
        raise NotImplementedError()

    def set(self, key: str, value:  str):
        raise NotImplementedError()

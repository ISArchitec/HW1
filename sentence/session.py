class Session:
    """Storage for environmental variables and potentially other session-specific parameters"""

    def __init__(self):
        self.__variables = dict()

    def get(self, key: str) -> str:
        return self.__variables.get(key, "")

    def set(self, key: str, value:  str):
        self.__variables[key] = value

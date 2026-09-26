class Session:
    """Storage for environmental variables and potentially other session-specific parameters"""

    def __init__(self):
        self.__variables = dict()

    def copy(self):
        session = Session()
        for key in self.__variables:
            session.set(key, self.__variables[key])
        return session

    def get(self, key: str) -> str:
        return self.__variables.get(key, "")

    def set(self, key: str, value:  str):
        self.__variables[key] = value

    def apply(self, env) -> None:
        for key in self.__variables:
            env[key] = self.__variables[key]

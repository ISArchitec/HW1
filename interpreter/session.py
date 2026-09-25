class Session:
    def get(self, key: str) -> str:
        raise NotImplementedError()

    def set(self, key: str, value:  str):
        raise NotImplementedError()

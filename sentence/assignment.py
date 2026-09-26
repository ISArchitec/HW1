from sentence.word import Word
from utils.session import Session
import os


class Assignment:
    def __init__(self, key: str, value: Word): # TODO(verbinna22): must be word
        self.__key = key
        self.__value = value

    @property
    def key(self) -> str:
        """Readonly access to assignment key"""
        return self.__key

    @property
    def value(self) -> Word:
        """Readonly access to assignment value"""
        return self.__value

    def execute(self, session: Session):
        """Changes session"""
        session.set(self.__key, self.__value.word)

    def apply_globally(self):
        """Changes global os environment"""
        os.environ[self.__key] = self.__value.word
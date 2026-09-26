from sentence.word import Word
from utils.session import Session
import os


class Assignment:
    def __init__(self, key: str, value: Word):
        self.key = key
        self.value = value

    def execute(self, session: Session):
        session.set(self.key, self.value.word)

    def apply_globally(self):
        os.environ[self.key] = self.value.word
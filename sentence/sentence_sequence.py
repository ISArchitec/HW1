from sentence.sentence import Sentence
from utils.session import Session
from stream import Console


class SentenceSequence:
    """Collection of sentences. Represents single line from interpreter, parsed into tokens"""

    __sentence: list[Sentence]

    def __init__(self, session: Session):
        self.__sentence = []
        self.session = session

    def add_sentence(self, sentence: Sentence) -> None:
        "adds sentence in sequence"
        self.__sentence.append(sentence)

    def __iter__(self):
        return iter(self.__sentence)

    def __len__(self):
        return len(self.__sentence)

    def __getitem__(self, key: int):
        return self.__sentence[key]

    def execute(self) -> None:
        """Executing all commands, that sequence represents"""
        console = Console()
        for sentence in self.__sentence:
            sentence.execute(self.session, console, console)
from sentence.sentence import Sentence
from stream import Console


class SentenceSequence:
    """Collection of sentences. Represents single line from interpreter, parsed into tokens"""

    __sentence: list[Sentence]

    def __init__(self):
        self.__sentence = []

    def add_sentence(self, sentence: Sentence) -> None:
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
            sentence.execute(console, console)
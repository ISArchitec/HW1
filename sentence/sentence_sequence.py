import asyncio

from sentence.sentence import Sentence
from stream import Console, Pipe
from utils.session import Session

MAX_PIPE_BUFFER = 100


class SentenceSequence:
    """Collection of sentences. Represents single line from interpreter, parsed into tokens"""

    __sentence: list[Sentence]

    def __init__(self, session: Session):
        self.__sentence = []
        self.session = session

    def add_sentence(self, sentence: Sentence) -> None:
        """Adds sentence in sequence"""
        self.__sentence.append(sentence)

    def __iter__(self):
        return iter(self.__sentence)

    def __len__(self):
        return len(self.__sentence)

    def __getitem__(self, key: int):
        return self.__sentence[key]

    async def execute(self) -> None:
        """Executing all commands, that sequence represents"""
        console = Console()
        streams = [Pipe(MAX_PIPE_BUFFER) for i in range(len(self.__sentence) - 1)]
        streams = [console, *streams, console]
        tasks = []
        for sentence_id in range(len(self.__sentence)):
            sentence = self.__sentence[sentence_id]
            exec_work = sentence.execute(
                self.session, streams[sentence_id], streams[sentence_id + 1]
            )
            tasks.append(asyncio.create_task(exec_work))
        await asyncio.gather(*tasks)

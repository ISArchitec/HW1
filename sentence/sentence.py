from sentence.word import Word
from sentence.assignment import Assignment
from utils.session import Session
from stream import InStream, OutStream
from command import CommandFactory


class Sentence:
    """Collection of words. Represents single command token"""

    def __init__(self, assignments: list[Assignment], words: list[Word]):
        self.__assignments = assignments.copy()
        self.__words = words.copy()

    @property
    def words(self):
        """Iterate over words in the sentence"""
        yield from self.__words

    @property
    def assignments(self):
        """Iterate over assignments in the sentence"""
        yield from self.__assignments

    def has_words(self) -> bool:
        """Check if there is no command in the sentence"""
        return len(self.__words) > 0

    def execute(self, session: Session, in_stream: InStream, out_stream: OutStream):
        """Executing command, that this sentence describe"""
        local_session = session.copy()
        for assignment in self.__assignments:
            if self.has_words():
                assignment.execute(local_session)
            else:
                assignment.apply_globally()
                assignment.execute(session)
        result_session = local_session if self.has_words() else session
        if self.has_words():
            CommandFactory().create(
                list(map(lambda word: word.word, self.__words)), in_stream, out_stream, result_session
            ).execute()

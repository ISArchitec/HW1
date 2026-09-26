from sentence.word import Word
from sentence.assignment import Assignment
from utils.session import Session
from stream import InStream, OutStream
from command import CommandFactory


class Sentence:
    """Collection of words. Represents single command token"""

    def __init__(self, assignments: list[Assignment], words: list[Word]):
        self.assignments = assignments.copy()
        self.reverted_assignments = list()
        self.words = words.copy()

    def has_words(self) -> bool:
        """Check if there is no command in the sentence"""
        return len(self.words) > 0

    def execute(self, session: Session, in_stream: InStream, out_stream: OutStream):
        """Executing command, that this sentence describe"""
        local_session = session.copy()
        for assignment in self.assignments:
            if self.has_words():
                assignment.execute(local_session)
            else:
                assignment.apply_globally()
                assignment.execute(session)
        result_session = local_session if self.has_words() else session
        if self.has_words():
            CommandFactory().create(
                list(map(lambda word: word.word, self.words)), in_stream, out_stream, result_session
            ).execute()

    def _remember_assignment(self, assignment: Assignment, session: Session):
        self.reverted_assignments.append(Assignment(assignment.key, Word(session.get(assignment.key))))

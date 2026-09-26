from sentence.word import Word
from sentence.assignment import Assignment
from sentence.session import Session
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
        for assignment in self.assignments:
            if self.has_words():
                self._remember_assignment(assignment, session)
            assignment.execute(session)
            assignment.apply_globally()
        if self.has_words():
            CommandFactory().create(list(map(lambda word: word.word, self.words)), in_stream, out_stream).execute()
        self._revert_assignments(session)

    def _remember_assignment(self, assignment: Assignment, session: Session):
        self.reverted_assignments.append(Assignment(assignment.key, Word(session.get(assignment.key))))

    def _revert_assignments(self, session: Session):
        while self.reverted_assignments:
            self.reverted_assignments[-1].apply_globally()
            self.reverted_assignments[-1].execute(session)
            self.reverted_assignments.pop()

from sentence.word import Word
from stream import InStream, OutStream
from command.command_factory import CommandFactory


class Sentence:
    """Collection of words. Represents single command token"""

    def __init__(self, words: list[Word]):
        # For now, there is no assignments and session
        self.words = words.copy()

    def has_words(self) -> bool:
        """Check if there is no command in the sentence"""
        return len(self.words) > 0

    def execute(self, in_stream: InStream, out_stream: OutStream):
        """Executing command, that this sentence describe"""
        CommandFactory().create(list(map(lambda word: word.word, self.words)), in_stream, out_stream).execute()

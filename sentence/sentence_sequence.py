from sentence.sentence import Sentence


class SentenceSequence:
    def __init__(self):
        # For now, there is no need to process multiple sentences
        self.sentence = None

    def add_sentence(self, sentence: Sentence) -> None:
        self.sentence = sentence

    def execute(self) -> None:
        if self.sentence is not None:
            self.sentence.execute()

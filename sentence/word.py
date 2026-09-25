class Word:
    """Minimal parsing component/token. Can be a word or a group of words in quotes. Basically, an alias for a string"""

    def __init__(self, word: str):
        self.word = word

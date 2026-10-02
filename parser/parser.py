from sentence import SentenceSequence, Sentence, Word
from sentence import Assignment
from utils.session import Session

from parser.pipes.pipe_splitter import PipeSplitter
from parser.substitution.substitutor import Substitutor
from parser.word_splitter.word_splitter import WordSplitter
from parser.utils.utils import is_token_symbol

class Parser:
    """Class, that parses line from interpreter into sentence sequence"""

    __session: Session

    def __init__(self, session: Session):
        self.__session = session

    def parse(self, string: str) -> SentenceSequence:
        """Main method of class, that parses line into sentence sequence"""
        sequence = SentenceSequence(self.__session)
        sentences = self.__parse_pipes(string)
        for sentence in sentences:
            words = self.__parse_whitespaces(self.__substitute(sentence))
            sequence.add_sentence(self.__make_sentence(words))
        return sequence

    def __parse_pipes(self, string: str) -> list[str]:
        string = string.strip()
        if len(string) == 0:
            return []
        splitter = PipeSplitter()
        for symbol in string:
            splitter.add_symbol(symbol)
        return list(splitter)

    def __substitute(self, sentence: str) -> str:
        substitutor = Substitutor(self.__session)
        for symbol in sentence:
            substitutor.add_symbol(symbol)
        return str(substitutor)

    def __parse_whitespaces(self, sentence: str) -> list[str]:
        splitter = WordSplitter()
        for symbol in sentence:
            splitter.add_symbol(symbol)
        return list(splitter)

    def __make_sentence(self, words: list[str]) -> Sentence:
        assignments = []
        command_words = []
        for i, word in enumerate(words):
            if not isinstance(parsing_result := self.__parse_element(word), Assignment):
                command_words = list(map(self.__parse_word, words[i:]))
                break
            assignments.append(parsing_result)
        return Sentence(assignments, command_words)

    def __parse_word(self, word: str) -> Word:
        return Word(word)

    def __parse_element(self, word: str) -> Assignment | Word:
        for (i, symbol) in enumerate(word):
            if not is_token_symbol(symbol, i):
                if symbol != '=' or i == 0:
                    return Word(word)
                else:
                    return Assignment(word[:i], Word(word[i + 1 :]))
        return Word(word)

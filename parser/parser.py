from typing import Self
from sentence import SentenceSequence, Sentence, Word
from enum import Enum, auto
from interpreter.session import Session

class ParsingMode(Enum):
    NORMAL = auto()
    QUOTED = auto()
    DOUBLE_QUOTED = auto()
    SKIP = auto()

class Parser:
    def __init__(self: Self, session: Session):
        pass

    def parse(self: Self, string: str) -> SentenceSequence:
        words = self.__parse_whitespaces(string)
        sentence = SentenceSequence()
        sentence.add_sentence(self.__make_sentence(words))
        return sentence

    def __parse_whitespaces(self: Self, sentence: str) -> list[str]:
        result = []
        parsing_mode = ParsingMode.SKIP
        for symbol in sentence:
            if parsing_mode == ParsingMode.SKIP:
                if symbol == '\'':
                    parsing_mode = ParsingMode.QUOTED
                    result.append('')
                elif symbol == '\"':
                    parsing_mode = ParsingMode.DOUBLE_QUOTED
                    result.append('')
                elif symbol != ' ':
                    parsing_mode = ParsingMode.NORMAL
                    result.append(symbol)
            elif parsing_mode == ParsingMode.QUOTED:
                if symbol == '\'':
                    parsing_mode = ParsingMode.NORMAL
                else:
                    result[-1] += symbol
            elif parsing_mode == ParsingMode.DOUBLE_QUOTED:
                if symbol == '\'':
                    parsing_mode = ParsingMode.NORMAL
                else:
                    result[-1] += symbol
            else:
                if symbol == ' ':
                    parsing_mode = ParsingMode.SKIP
                else:
                    result[-1] += symbol
        return result

    def __make_sentence(self: Self, words: list[str]) -> Sentence:
        return Sentence(list(map(self.__parse_element, words)))

    def __parse_element(self: Self, word: str) -> Word:
        return Word(word)

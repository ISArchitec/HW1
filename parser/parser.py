from sentence import SentenceSequence, Sentence, Word
from enum import Enum, auto
from interpreter.session import Session
from utils.exception import ParserError


class ParsingMode(Enum):
    # simple token parsing
    NORMAL = auto()
    # '...'
    QUOTED = auto()
    # "..."
    DOUBLE_QUOTED = auto()
    # skip whitespaces between words
    SKIP = auto()


class Parser:
    __session: Session

    def __init__(self, session: Session):
        self.__session = session

    def parse(self, string: str) -> SentenceSequence:
        sequence = SentenceSequence()
        sentences = self.__parse_pipes(string)
        for sentence in sentences:
            words = self.__parse_whitespaces(sentence)
            sequence.add_sentence(self.__make_sentence(words))
        return sequence

    def __parse_pipes(self, string: str) -> list[str]:
        string = string.strip()
        if len(string) == 0:
            return []
        else:
            return [string]

    def __parse_whitespaces(self, sentence: str) -> list[str]:
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
                elif not symbol.isspace():
                    parsing_mode = ParsingMode.NORMAL
                    result.append(symbol)
            elif parsing_mode == ParsingMode.QUOTED:
                if symbol == '\'':
                    parsing_mode = ParsingMode.NORMAL
                else:
                    result[-1] += symbol
            elif parsing_mode == ParsingMode.DOUBLE_QUOTED:
                if symbol == '\"':
                    parsing_mode = ParsingMode.NORMAL
                else:
                    result[-1] += symbol
            else:
                if symbol.isspace():
                    parsing_mode = ParsingMode.SKIP
                elif symbol == '\'':
                    parsing_mode = ParsingMode.QUOTED
                elif symbol == '\"':
                    parsing_mode = ParsingMode.DOUBLE_QUOTED
                else:
                    result[-1] += symbol
        if parsing_mode in (ParsingMode.QUOTED, ParsingMode.DOUBLE_QUOTED):
            raise ParserError("Unclosed quote")
        if len(result) == 0:
            raise ParserError("Sentence couldn't be empty")
        return result

    def __make_sentence(self, words: list[str]) -> Sentence:
        return Sentence(list(map(self.__parse_element, words)))

    def __parse_element(self, word: str) -> Word:
        return Word(word)

import pytest

from parser import Parser
from interpreter.session import Session
from utils.exception import ParserError

EMPTY_SESSION = Session()

def parse_words(source: str) -> list[str]:
    parser = Parser(session=EMPTY_SESSION)
    sequence = parser.parse(source)

    assert len(sequence) == 1
    return [word.word for word in sequence[0].words]


@pytest.mark.parametrize(
    "source, expected",
    [
        ("echo", ["echo"]),
        ("echo hello world", ["echo", "hello", "world"]),
        ("  echo   hello  ", ["echo", "hello"]),

        ("echo 'hello world'", ["echo", "hello world"]),
        ("'hello world'", ["hello world"]),
        ("'hello world'\n", ["hello world"]),
        ("'hello' world", ["hello", "world"]),
        ("''", [""]),

        ('echo "hello world"', ["echo", "hello world"]),
        ('"hello world"', ["hello world"]),
        ('"hello" world', ["hello", "world"]),
        ('""', [""]),

        ("echo '\"hello world\"'", ["echo", '"hello world"']),
        ('echo "it\'s fine"', ["echo", "it's fine"]),
        ("echo 'it\"s fine'", ["echo", 'it"s fine']),
    ],
)
def test_parser_parses_words_and_quotes(source: str, expected: list[str]) -> None:
    assert parse_words(source) == expected

@pytest.mark.parametrize(
    "source",
    [
        "echo 'hello",
        "'hello",
        "echo \"hello",
        "\"hello",
        "echo 'hello world",
        "echo \"hello world",
        "hel'lo",
        "he\"llo",
        "echo hel'lo"
        "echo hel\"lo",
        "abc'",
        "abc\"",
    ],
)
def test_parser_raises_on_malformed_quotes(source: str) -> None:
    with pytest.raises(ParserError):
        parse_words(source)

def test_parser_no_sequence_on_empty_source():
    parser = Parser(session=EMPTY_SESSION)
    sequence = parser.parse("")
    assert len(sequence) == 0

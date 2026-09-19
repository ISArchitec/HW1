# tests/test_parser.py

import pytest

from parser import Parser


def parse_words(source: str) -> list[str]:
    parser = Parser(session=None)  # session в __init__ не используется
    sequence = parser.parse(source)

    assert sequence.sentence is not None
    return [word.word for word in sequence.sentence.words]


@pytest.mark.parametrize(
    "source, expected",
    [
        ("", []),
        ("echo", ["echo"]),
        ("echo hello world", ["echo", "hello", "world"]),
        ("  echo   hello  ", ["echo", "hello"]),

        ("echo 'hello world'", ["echo", "hello world"]),
        ("'hello world'", ["hello world"]),
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

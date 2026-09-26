import pytest

from parser import Parser
from utils.session import Session
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

def parse_assignments(source: str) -> list[tuple[str, str]]:
    parser = Parser(session=EMPTY_SESSION)
    sequence = parser.parse(source)
    assert len(sequence) == 1
    return [(a.key, a.value.word) for a in sequence[0].assignments]


@pytest.mark.parametrize(
    "source, expected",
    [
        ("X=1", [("X", "1")]),
        ("NAME=hello", [("NAME", "hello")]),
        ("_=v", [("_", "v")]),
        ("VAR1=abc", [("VAR1", "abc")]),
        ("A_B_C=xyz", [("A_B_C", "xyz")]),
        ("X=1 Y=2", [("X", "1"), ("Y", "2")]),
        ("A=1 B=2 C=3", [("A", "1"), ("B", "2"), ("C", "3")]),
        ("  X=1   Y=2  ", [("X", "1"), ("Y", "2")]),
        ("X=", [("X", "")]),
        ("X=a=b", [("X", "a=b")]),
        ("X==", [("X", "=")]),
        ("X='hello world'", [("X", "hello world")]),
        ('X="hello world"', [("X", "hello world")]),
        ("X=''", [("X", "")]),
        ('X=""', [("X", "")]),
        ("X='a=b'", [("X", "a=b")]),
        ('X="a=b"', [("X", "a=b")]),
        ("X=/usr/bin", [("X", "/usr/bin")]),
        ("X=*.txt", [("X", "*.txt")]),
        ("X=$HOME", [("X", "$HOME")]),
        ("X=1 echo", [("X", "1")]),
        ("X=1 Y=2 echo hello", [("X", "1"), ("Y", "2")]),
        ("X=1 echo Y=2", [("X", "1")]),
        ("echo X=1", []),
        ("echo hello world", []),
        ("echo", []),
        ("X=1 echo 'hello world'", [("X", "1")]),
        ("X = 1", []),
        ("X =1", []),
        ("X= 1", [("X", "")]),
    ],
)
def test_parser_parses_assignments(source: str, expected: list[tuple[str, str]]) -> None:
    assert parse_assignments(source) == expected

def parse(source: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Parse `source` и вернуть (assignments, words) единственного предложения."""
    sequence = Parser(session=EMPTY_SESSION).parse(source)
    assert len(sequence) == 1
    sentence = sequence[0]
    assignments = [(a.key, a.value.word) for a in sentence.assignments]
    words = [w.word for w in sentence.words]
    return assignments, words


@pytest.mark.parametrize(
    "source, expected_assignments, expected_words",
    [
        ("  echo   hello  ", [], ["echo", "hello"]),
        ("  X=1   Y=2  ", [("X", "1"), ("Y", "2")], []),
        ("X=1 echo 'hello world'", [("X", "1")], ["echo", "hello world"]),
        ("echo X=1", [], ["echo", "X=1"]),
        ("echo hello X=1", [], ["echo", "hello", "X=1"]),
        ("X=1 echo Y=2", [("X", "1")], ["echo", "Y=2"]),
        ("X=1 Y=2 echo Z=3", [("X", "1"), ("Y", "2")], ["echo", "Z=3"]),
        ("X= 1", [("X", "")], ["1"]),
        ("1X=1", [], ["1X=1"]),
        ("X1=1", [("X1", "1")], []),
        ("X-Y=1", [], ["X-Y=1"]),
        ("=1", [], ["=1"]),
        ("X@Y=1", [], ["X@Y=1"]),
        ("_X=1", [("_X", "1")], []),
    ],
)
def test_parser_assignments_and_words(
    source: str,
    expected_assignments: list[tuple[str, str]],
    expected_words: list[str],
) -> None:
    assignments, words = parse(source)
    assert assignments == expected_assignments
    assert words == expected_words

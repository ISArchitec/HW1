from unittest.mock import patch
import pytest

from stream import Console, InStream, OutStream


def test_read_line_reads_from_input():
    console = Console()
    with patch("builtins.input", return_value="echo hi"):
        assert console.read_line() == "echo hi"


def test_read_char_returns_first_char():
    console = Console()
    with patch("builtins.input", return_value="abc") as fake_input:
        assert console.read_char() == "a"
        assert fake_input.call_count == 1


def test_read_line_after_read_char_returns_rest():
    console = Console()
    with patch("builtins.input", return_value="abc"):
        console.read_char()
        assert console.read_line() == "bc"


def test_write_outputs_text_verbatim(capsys):
    Console().write("hi\n")
    assert capsys.readouterr().out == "hi\n"

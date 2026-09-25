from unittest.mock import patch

import pytest

from interpreter.global_console import GlobalConsole
from interpreter.interpreter import Interpreter
from interpreter.session import Session
from stream import Console


def test_global_console_uses_console_streams():
    console = GlobalConsole()
    for stream in (console.stdin, console.stdout, console.stderr):
        assert isinstance(stream, Console)


def test_session_is_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        Session().get("x")
    with pytest.raises(NotImplementedError):
        Session().set("x", "1")


class StopLoop(BaseException):
    """Not an Exception subclass: gets past `except Exception` and ends the loop."""


def run_interpreter(lines):
    with patch("builtins.input", side_effect=[*lines, StopLoop]):
        Interpreter().run()


def test_parser_error_is_printed_and_loop_continues(capsys):
    with pytest.raises(StopLoop):
        run_interpreter(["echo 'unclosed"])
    assert "Unclosed quote" in capsys.readouterr().out


@pytest.mark.xfail(strict=True, raises=StopLoop,
                   reason="bug #1: commands never run from the interpreter")
def test_exit_command_stops_interpreter():
    with pytest.raises(SystemExit) as raised:
        run_interpreter(["exit"])
    assert raised.value.code == 0


@pytest.mark.xfail(strict=True, raises=StopLoop,
                   reason="bug #3: EOF is swallowed, loop never stops")
def test_eof_stops_interpreter():
    run_interpreter([EOFError])

from unittest.mock import patch
import pytest
from interpreter.interpreter import Interpreter


class StopLoop(BaseException):
    """Not an Exception subclass: gets past `except Exception` and ends the loop."""


def run_interpreter(lines):
    with patch("builtins.input", side_effect=[*lines, StopLoop]):
        Interpreter().run()


def test_parser_error_is_printed_and_loop_continues(capsys):
    with pytest.raises(StopLoop):
        run_interpreter(["echo 'unclosed"])
    assert "Unclosed quote" in capsys.readouterr().out


def test_exit_command_stops_interpreter():
    with pytest.raises(SystemExit) as raised:
        run_interpreter(["exit"])
        assert raised.value.code == 0


def test_base_command_works_interpreter(capsys):
    with pytest.raises(SystemExit) as raised:
        run_interpreter(["echo 'hi'", "exit"])
        assert "'hi'" in capsys.readouterr().out
        assert raised.value.code == 0
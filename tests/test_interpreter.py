from unittest.mock import patch

import pytest

from interpreter.interpreter import Interpreter


class StopLoop(BaseException):
    """Not an Exception subclass: gets past `except Exception` and ends the loop."""


async def run_interpreter(lines):
    with patch("aioconsole.ainput", side_effect=[*lines, StopLoop]):
        await Interpreter().run()


async def test_parser_error_is_printed_and_loop_continues(capsys):
    with pytest.raises(StopLoop):
        await run_interpreter(["echo 'unclosed"])
    assert "Unclosed quote" in capsys.readouterr().out


async def test_exit_command_stops_interpreter():
    await run_interpreter(["exit"])


async def test_base_command_works_interpreter(capsys):
    await run_interpreter(["echo 'hi'", "exit"])
    assert "hi" in capsys.readouterr().out

from unittest.mock import patch

from stream import Console


async def test_read_line_reads_from_input():
    console = Console()
    with patch("aioconsole.ainput", return_value="echo hi"):
        assert await console.read_line() == "echo hi"


async def test_read_char_returns_first_char():
    console = Console()
    with patch("aioconsole.ainput", return_value="abc") as fake_input:
        assert await console.read_char() == "a"
        assert fake_input.call_count == 1


async def test_read_line_after_read_char_returns_rest():
    console = Console()
    with patch("aioconsole.ainput", return_value="abc"):
        await console.read_char()
        assert await console.read_line() == "bc"


async def test_write_outputs_text_verbatim(capsys):
    await Console().write("hi\n")
    assert capsys.readouterr().out == "hi\n"

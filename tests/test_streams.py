import asyncio
from unittest.mock import patch

import pytest

from command import CommandFactory
from stream import Console, Pipe
from tests.helpers import MemoryStream, cleanup_tasks


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Console.read_line strips the newline, including on blank input",
)
@pytest.mark.parametrize("line", ["echo hi", ""])
async def test_read_line_reads_from_input(line):
    console = Console()
    with patch("aioconsole.ainput", return_value=line):
        assert await console.read_line() == line + "\n"


@pytest.mark.xfail(
    strict=True,
    raises=EOFError,
    reason="Console propagates EOFError instead of returning an empty string",
)
async def test_console_eof_returns_empty_string():
    console = Console()
    with patch("aioconsole.ainput", side_effect=EOFError):
        assert await console.read_line() == ""


async def test_write_outputs_text_verbatim(capsys):
    await Console().write("hi\n")
    assert capsys.readouterr().out == "hi\n"


async def test_pipe_preserves_write_order():
    pipe = Pipe(2)
    await pipe.write("first\n")
    await pipe.write("second\n")
    assert await asyncio.wait_for(pipe.read_line(), 1) == "first\n"
    assert await asyncio.wait_for(pipe.read_line(), 1) == "second\n"


async def test_pipe_blocks_writer_until_reader_frees_space():
    pipe = Pipe(1)
    await pipe.write("first\n")
    async with cleanup_tasks():
        writer = asyncio.create_task(pipe.write("second\n"))
        await asyncio.sleep(0)
        assert not writer.done()
        assert await pipe.read_line() == "first\n"
        await asyncio.wait_for(writer, 1)
        assert await pipe.read_line() == "second\n"


async def test_pipe_waiting_reader_receives_later_write():
    pipe = Pipe(1)
    async with cleanup_tasks():
        reader = asyncio.create_task(pipe.read_line())
        await asyncio.sleep(0)
        assert not reader.done()
        await pipe.write("later\n")
        assert await asyncio.wait_for(reader, 1) == "later\n"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Pipe enqueues empty writes and exposes them as false EOF",
)
async def test_pipe_empty_write_does_not_end_input():
    pipe = Pipe(2)
    await pipe.write("")
    await pipe.write("data\n")
    assert await asyncio.wait_for(pipe.read_line(), 1) == "data\n"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Console strips newlines and treats a blank line as EOF for commands",
)
async def test_console_input_preserves_lines_for_wc(session):
    output = MemoryStream()
    with patch("aioconsole.ainput", side_effect=["hello", "", "world", EOFError]):
        command = CommandFactory().create(["wc", "-lw"], Console(), output, session)
        await command.execute()
    assert output.buffer.getvalue() == "3 2\n"

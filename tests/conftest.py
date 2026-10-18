import asyncio

import pytest

from command import CommandFactory
from tests.helpers import MemoryStream
from utils.session import Session


@pytest.fixture
def session():
    return Session()


@pytest.fixture
def run_command(session):
    async def run(words, text=""):
        output = MemoryStream()
        command = CommandFactory().create(words, MemoryStream(text), output, session)
        await asyncio.wait_for(command.execute(), timeout=10)
        return output.buffer.getvalue()

    return run

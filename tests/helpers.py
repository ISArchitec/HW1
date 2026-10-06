import asyncio
import io
from contextlib import asynccontextmanager

from stream import InStream, OutStream


@asynccontextmanager
async def cleanup_tasks():
    baseline = asyncio.all_tasks()
    try:
        yield
    finally:
        pending = [
            task
            for task in asyncio.all_tasks() - baseline
            if task is not asyncio.current_task() and not task.done()
        ]
        for task in pending:
            task.cancel()
        await asyncio.wait_for(asyncio.gather(*pending, return_exceptions=True), timeout=10)


class MemoryStream(InStream, OutStream):
    def __init__(self, text: str = ""):
        self.buffer = io.StringIO(text)

    async def read_char(self) -> str:
        return self.buffer.read(1)

    async def read_line(self) -> str:
        return self.buffer.readline()

    async def write(self, string: str) -> None:
        self.buffer.write(string)

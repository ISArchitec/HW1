import asyncio
import codecs
import os
from contextlib import suppress

from command.command import CHUNK_SIZE, Command
from stream import Console, InStream, OutStream
from utils.exception import ExecutionError
from utils.session import Session


class ExecCommand(Command):
    """Run an external program and forward its standard input and output."""

    def __init__(
        self, args: list[str], in_stream: InStream, out_stream: OutStream, session: Session
    ):
        super().__init__(args, in_stream, out_stream)
        self.session = session

    async def execute(self) -> None:
        """Launch the program and map launch or exit failures to ExecutionError."""
        process = await self._start_process()
        input_task = asyncio.create_task(self._forward_input(process))
        output_task = asyncio.create_task(self._forward_output(process))
        wait_task = asyncio.create_task(process.wait())
        tasks: list[asyncio.Task[int | None]] = [input_task, output_task, wait_task]
        pending = set(tasks)

        try:
            while pending:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    task.result()
                if wait_task in done and input_task in pending:
                    # Stop feeding the finished process, but drain its remaining output.
                    input_task.cancel()
                    pending.remove(input_task)

            returncode = wait_task.result()
            if returncode != 0:
                raise ExecutionError(returncode)
        except (OSError, UnicodeError) as error:
            raise ExecutionError(1) from error
        finally:
            await self._cleanup(process, tasks)

    async def _start_process(self) -> asyncio.subprocess.Process:
        sub_env = os.environ.copy()
        self.session.apply(sub_env)
        try:
            return await asyncio.create_subprocess_exec(
                *self.args,
                stdin=None if isinstance(self.in_stream, Console) else asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                env=sub_env,
            )
        except FileNotFoundError as error:
            raise ExecutionError(127) from error
        except OSError as error:
            raise ExecutionError(126) from error

    @staticmethod
    async def _cleanup(
        process: asyncio.subprocess.Process, tasks: list[asyncio.Task[int | None]]
    ) -> None:
        for task in tasks:
            if not task.done():
                task.cancel()
        if process.returncode is None:
            with suppress(ProcessLookupError):
                process.kill()
        await asyncio.gather(*tasks, return_exceptions=True)
        await process.wait()

    async def _forward_input(self, process: asyncio.subprocess.Process) -> None:
        if process.stdin is None:
            return
        try:
            async for chunk in self._read_chunks():
                process.stdin.write(chunk.encode("utf-8"))
                await process.stdin.drain()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            process.stdin.close()

    async def _forward_output(self, process: asyncio.subprocess.Process) -> None:
        if process.stdout is None:
            raise ExecutionError(1)
        decoder = codecs.getincrementaldecoder("utf-8")()
        chunk = await process.stdout.read(CHUNK_SIZE)
        while chunk:
            text = decoder.decode(chunk)
            if text:
                await self._write(text)
            chunk = await process.stdout.read(CHUNK_SIZE)
        tail = decoder.decode(b"", final=True)
        if tail:
            await self._write(tail)

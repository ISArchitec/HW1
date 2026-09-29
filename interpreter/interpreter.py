from interpreter.global_console import GlobalConsole
from parser import Parser
from utils.exception import CliError, ExitInterrupt
from utils.session import Session


class Interpreter:
    """Manages all processes in interpreter. It reads users inputs, process it, and writes output"""

    async def run(self) -> None:
        """Main program loop"""
        running = True
        console = GlobalConsole()
        session = Session()
        parser = Parser(session)
        while running:
            try:
                input = await console.stdin.read_line()
                sequence = parser.parse(input)
                await sequence.execute()
            except ExitInterrupt:
                running = False
            except CliError as e:
                print(e)
            except Exception as e:
                print("Unexpected error occurred:")
                print(e)

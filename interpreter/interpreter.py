from interpreter.global_console import GlobalConsole
from parser import Parser
from utils.exception import CliError
from interpreter.session import Session


class Interpreter:
    """Manages all processes in interpreter. It reads users inputs, process it, and writes output"""

    def run(self) -> None:
        """Main program loop"""
        running = True
        console = GlobalConsole()
        session = Session()
        parser = Parser(session)
        while running:
            try:
                input = console.stdin.read_line()
                sequence = parser.parse(input)
                sequence.execute()
            except CliError as e:
                print(e)
            except Exception as e:
                print("Unexpected error occurred:")
                print(e)

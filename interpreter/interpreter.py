from global_console import GlobalConsole
from parser.parser import Parser
from utils.exception import CliError


class Interpreter:
    def run(self) -> None:
        running = True
        console = GlobalConsole()
        parser = Parser()
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

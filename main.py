import asyncio

from interpreter import Interpreter


async def main():
    interpreter = Interpreter()
    await interpreter.run()


if __name__ == "__main__":
    asyncio.run(main())

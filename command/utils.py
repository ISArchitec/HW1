from utils.exception import ExecutionError


def parse_options(args: list[str], allowed: set[str]) -> tuple[set[str], list[str]]:
    options: set[str] = set()
    files: list[str] = []
    parse_flags = True
    for arg in args:
        if parse_flags and arg == "--":
            parse_flags = False
        elif parse_flags and arg.startswith("-") and arg != "-":
            flags = set(arg[1:])
            if not flags <= allowed:
                raise ExecutionError(1)
            options.update(flags)
        else:
            files.append(arg)
    return options, files

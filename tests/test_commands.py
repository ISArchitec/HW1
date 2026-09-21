import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from command.command_factory import CommandFactory
from command.builtins import EchoCommand
from command.exec_command import ExecCommand
from stream import InStream, OutStream
from utils.exception import ExecutionError


class MemoryStream(InStream, OutStream):
    def __init__(self, text=""):
        self.buffer = io.StringIO(text)

    def read_char(self):
        return self.buffer.read(1)

    def read_line(self):
        return self.buffer.readline()

    def write(self, string):
        self.buffer.write(string)


class CommandTests(unittest.TestCase):
    def test_output_errors_become_execution_errors(self):
        error = OSError("write failed")
        for words in [["cat"], ["cat", "-n"], ["echo", "hello"], ["wc"], ["pwd"]]:
            with self.subTest(words=words):
                source, output = MemoryStream("hello\n"), MemoryStream()
                command = CommandFactory().create(words, source, output)
                with patch.object(output, "write", side_effect=error):
                    with self.assertRaises(ExecutionError) as raised:
                        command.execute()
                self.assertEqual(raised.exception.code, 1)

    def execute_command(self, words, text=""):
        source, output = MemoryStream(text), MemoryStream()
        CommandFactory().create(words, source, output).execute()
        return output.buffer.getvalue()

    def test_pwd(self):
        self.assertEqual(self.execute_command(["pwd"]), os.getcwd() + "\n")
        with self.assertRaises(ExecutionError) as raised:
            self.execute_command(["pwd", "unexpected"])
        self.assertEqual(raised.exception.code, 1)
        with patch("command.builtins.pwd.os.getcwd", side_effect=OSError):
            with self.assertRaises(ExecutionError):
                self.execute_command(["pwd"])

    def test_exit(self):
        command = CommandFactory().create(["exit"], MemoryStream(), MemoryStream())
        with self.assertRaises(SystemExit) as raised:
            command.execute()
        self.assertEqual(raised.exception.code, 0)

    def test_factory_selects_external_command(self):
        command = CommandFactory().create(
            ["external-program"], MemoryStream(), MemoryStream()
        )
        self.assertIsInstance(command, ExecCommand)

    def test_external_arguments(self):
        script = (
            "import sys; from pathlib import Path; "
            "Path(sys.argv[1]).write_text(sys.argv[2], encoding='utf-8')"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "output.txt"
            self.execute_command(
                [sys.executable, "-c", script, str(path), "a b; $name"]
            )
            self.assertEqual(path.read_text(encoding="utf-8"), "a b; $name")

    def test_external_nonzero_exit(self):
        with self.assertRaises(ExecutionError) as raised:
            self.execute_command([sys.executable, "-c", "raise SystemExit(3)"])
        self.assertEqual(raised.exception.code, 3)

    def test_external_missing_program(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ExecutionError) as raised:
                self.execute_command([str(Path(directory) / "missing-program")])
        self.assertEqual(raised.exception.code, 127)

    def test_external_launch_permission_error(self):
        with patch("command.exec_command.subprocess.run", side_effect=PermissionError):
            with self.assertRaises(ExecutionError) as raised:
                self.execute_command(["external-program"])
        self.assertEqual(raised.exception.code, 126)

    def test_echo(self):
        self.assertEqual(self.execute_command(["echo"]), "\n")
        self.assertEqual(
            self.execute_command(["echo", "hello world", "", "$name"]),
            "hello world  $name\n",
        )

    def test_factory_creates_without_executing_and_copies_arguments(self):
        output = MemoryStream()
        words = ["echo", "original"]
        command = CommandFactory().create(words, MemoryStream(), output)
        self.assertIsInstance(command, EchoCommand)
        self.assertEqual(output.buffer.getvalue(), "")
        words[1] = "changed"
        command.execute()
        self.assertEqual(output.buffer.getvalue(), "original\n")

    def test_factory_errors(self):
        with self.assertRaises(ValueError):
            self.execute_command([])

    def test_cat_stdin_preserves_text(self):
        for text in ["", "\n", "one\r\n\ntwo", "no final newline"]:
            with self.subTest(text=text):
                self.assertEqual(self.execute_command(["cat"], text), text)

    def test_multiple_files(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a.txt", Path(directory) / "b.txt"
            first.write_bytes(b"hi\r\n")
            second.write_bytes(b"end")
            self.assertEqual(
                self.execute_command(["cat", str(first), str(second)], "unused input"),
                "hi\r\nend",
            )
            self.assertEqual(
                self.execute_command(["wc", str(first), str(second)]),
                f"1 1 4 {first}\n0 1 3 {second}\n1 2 7 total\n",
            )

    def test_wc_stdin(self):
        for text, expected in [
            ("", "0 0 0\n"),
            ("\n", "1 0 1\n"),
            ("one\ttwo\nlast", "1 3 12\n"),
            ("word", "0 1 4\n"),
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.execute_command(["wc"], text), expected)

    def test_wc_word_crossing_chunk_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "long.txt"
            path.write_bytes(b"a" * 9000 + b" b\n")
            self.assertEqual(
                self.execute_command(["wc", str(path)]), f"1 2 9003 {path}\n"
            )

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.txt"
            for name in ["cat", "wc"]:
                with self.subTest(name=name):
                    with self.assertRaises(ExecutionError) as raised:
                        self.execute_command([name, str(path)])
                    self.assertEqual(raised.exception.code, 1)

    def test_echo_option_order_and_text(self):
        cases = [
            (["-n", "hello"], "hello"),
            (["-n"], ""),
            (["-ne", r"one\ntwo"], "one\ntwo"),
            (["-e", "-E", r"one\ntwo"], "one\\ntwo\n"),
            (["-E", "-e", r"one\ntwo"], "one\ntwo\n"),
            (["-eE", r"\t"], "\\t\n"),
            (["hello", "-n"], "hello -n\n"),
            (["-no", "-n"], "-no -n\n"),
            (["--", "-n"], "-- -n\n"),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(self.execute_command(["echo", *args]), expected)

    def test_echo_escapes(self):
        cases = [
            (r"a\cb", "a"),
            (r"\a\b\e\f\n\r\t\v\\", "\a\b\x1b\f\n\r\t\v\\\n"),
            (r"\0101\x42", "AB\n"),
            (r"\0", "\0\n"),
            (r"\q\x", "\\q\\x\n"),
            ("hello\\", "hello\\\n"),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(self.execute_command(["echo", "-e", text]), expected)

    def test_cat_numbering_and_squeeze(self):
        text = "a\n\n\nb\n"
        self.assertEqual(self.execute_command(["cat", "-n"], text),
                         "     1\ta\n     2\t\n     3\t\n     4\tb\n")
        self.assertEqual(self.execute_command(["cat", "-bn"], text),
                         "     1\ta\n\n\n     2\tb\n")
        self.assertEqual(self.execute_command(["cat", "-sn"], text),
                         "     1\ta\n     2\t\n     3\tb\n")

    def test_cat_visible_characters(self):
        self.assertEqual(self.execute_command(["cat", "-ET"], "a\t\nlast"), "a^I$\nlast")
        self.assertEqual(self.execute_command(["cat", "-v"], "\0\x1b\x7f\t\n"), "^@^[^?\t\n")
        self.assertEqual(self.execute_command(["cat", "-A"], "\0\t\r\n"), "^@^I^M$\n")

    def test_cat_state_across_files_and_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a", Path(directory) / "b"
            first.write_bytes(b"a" * 8193)
            second.write_bytes(b"b\n\n\nc")
            self.assertEqual(
                self.execute_command(["cat", "-ns", str(first), str(second)]),
                "     1\t" + "a" * 8193 + "b\n     2\t\n     3\tc",
            )
            first.write_bytes(b"a\n\n")
            second.write_bytes(b"\n\nb")
            self.assertEqual(self.execute_command(["cat", "-s", str(first), str(second)]), "a\n\nb")

    def test_wc_selected_counts_and_order(self):
        text = "a b\n"
        for args, expected in [
            (["-l"], "1\n"), (["-w"], "2\n"), (["-m"], "4\n"),
            (["-c"], "4\n"), (["-cmwl"], "1 2 4 4\n"),
            (["-l", "-w", "-l"], "1 2\n"), (["-L"], "3\n"),
        ]:
            with self.subTest(args=args):
                self.assertEqual(self.execute_command(["wc", *args], text), expected)

    def test_wc_display_width(self):
        self.assertEqual(self.execute_command(["wc", "-L"], "a\tb\nhello"), "9\n")
        self.assertEqual(self.execute_command(["wc", "-L"], ""), "0\n")
        self.assertEqual(self.execute_command(["wc", "-L"], "abc\rx"), "3\n")

    def test_wc_totals_use_maximum_width(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a", Path(directory) / "b"
            first.write_bytes(b"abcd\n")
            second.write_bytes(b"xy\n")
            self.assertEqual(
                self.execute_command(["wc", "-lL", str(first), str(second)]),
                f"1 4 {first}\n1 2 {second}\n2 4 total\n",
            )

    def test_double_dash_preserves_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "-n").write_bytes(b"abc\n")
            previous_directory = os.getcwd()
            try:
                os.chdir(directory)
                self.assertEqual(self.execute_command(["cat", "--", "-n"]), "abc\n")
                self.assertEqual(self.execute_command(["wc", "--", "-n"]), "1 1 4 -n\n")
            finally:
                os.chdir(previous_directory)

    def test_invalid_options(self):
        for name in ["cat", "wc"]:
            with self.subTest(name=name), self.assertRaises(ExecutionError) as raised:
                self.execute_command([name, "-z"])
            self.assertEqual(raised.exception.code, 1)


if __name__ == "__main__":
    unittest.main()

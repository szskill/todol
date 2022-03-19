import unittest
import subprocess
import os


class InvalidStateTest(unittest.TestCase):
    def test_invalid_state_char(self) -> None:
        """Tests for an state character, like `[y]` where `y` is supposed to be `x`"""

        cases = (
            "[y]",
            "[ [",
            "[-",
            "sus",
            "?",
        )

        for case in cases:
            with open("TEST_TODO", "w") as f:
                f.write(case)

            try:
                output = subprocess.check_output(
                    ["python", "todol.py", "TEST_TODO"]
                ).decode("utf-8")
            except subprocess.CalledProcessError as exc:
                output = exc.stdout.decode("utf-8")

            self.assertEqual(
                output, "TEST_TODO, line 1: Line does not start with [x] or [ ]\n"
            )

            os.remove("TEST_TODO")

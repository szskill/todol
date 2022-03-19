# TodoL is licensed under the MIT license
# https://github.com/szskill/todol

from __future__ import annotations

import json
import sys
from typing import Any, Iterable


class Todo:
    def __init__(self, todos: dict[str, bool] = {}) -> None:
        # Represents the todos. It's a dictionary storing the todo text as the
        # key and its current state as the value.
        self.todos = todos

    def to_json(self, pretty_print=True) -> str:
        """Turns this object into a JSON string."""

        dumps_kwargs = {}
        if pretty_print:
            dumps_kwargs["indent"] = 4

        return json.dumps(self.todos, **dumps_kwargs)

    @staticmethod
    def from_file(path: str) -> Todo:
        """Creates a new Todo object from a file."""

        with open(path) as f:
            content = f.read()

            todos: dict[str, bool] = {}
            for line_num, line in enumerate(content.splitlines()):
                if line.isspace() or line == "":
                    continue

                # Just for convenience in error messages
                line_num += 1

                if not line.startswith("[x]") or not line.startswith("[ ]"):
                    print(
                        f"{path}, line {line_num}: Line does not start with [x] or [ ]"
                    )
                    sys.exit(1)

                tokens = line.split()
                state = tokens[0] == "[x]"

                # line.split() will parse whitespace in [ ]
                if state:
                    text = " ".join(tokens[1:])
                else:
                    text = " ".join(tokens[2:])

                todos[text] = state

            return Todo(todos)


def index_with_default_value(iterable: Iterable, index: int, default_value: Any):
    """Gets the value at the index of the specified iterable, but if it's not
    possible then it falls back to the default value.
    """

    value = None
    if index < len(iterable):
        value = iterable[index]
    else:
        value = default_value

    return value


if __name__ == "__main__":
    path = index_with_default_value(sys.argv, 1, "TODO")
    output_language = index_with_default_value(sys.argv, 2, "json")

    try:
        todo = Todo.from_file(path)
    except FileNotFoundError:
        print(f'The file "{path}" does not exist.')
        sys.exit(1)

    if output_language == "json":
        print(todo.to_json())
    else:
        print(f'Invalid language "{output_language}"')
        sys.exit(1)

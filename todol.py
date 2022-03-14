from __future__ import annotations

import json
import sys


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
                if line.isspace() or line == '':
                    continue
                
                # Just for convenience
                line_num += 1

                tokens = line.split()
                state = tokens[0] == "[x]"

                # line.split() will parse whitespace in [ ]
                if state:
                    text = " ".join(tokens[1:])
                else:
                    text = " ".join(tokens[2:])

                todos[text] = state

            return Todo(todos)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else 'TODO'
    output_language = sys.argv[2] if len(sys.argv) > 2 else 'json'

    todo = Todo.from_file(path)

    if output_language == 'json':
        print(todo.to_json())
    else:
        print(f'Invalid language "{output_language}"')
        exit(1)
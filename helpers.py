def read_integer(prompt: str, minimum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Error: please enter a valid integer.')
            continue
        if minimum is None or value >= minimum:
            return value
        print(f'Error: value must be at least {minimum}.')


def read_text(prompt: str = 'Enter text: ') -> str:
    while True:
        text_example = input(prompt)
        if not text_example.strip():
            print('Error: text must not be empty or consist of spaces only!')
            continue
        return text_example

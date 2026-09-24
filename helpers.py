from collections.abc import Callable
from datetime import date, datetime
from constants import DATE_FORMAT

MenuOption = tuple[str, Callable[[], None]]


def parse_integer(text: str, minimum: int | None = None, maximum: int | None = None) -> int:
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f'not an integer: {text}') from None
    if minimum is not None and value < minimum:
        raise ValueError(f'must be at least {minimum}: {text}')
    if maximum is not None and value > maximum:
        raise ValueError(f'must be at most {maximum}: {text}')
    return value


def read_integer(prompt: str, minimum: int | None = None, maximum: int | None = None) -> int:
    while True:
        try:
            return parse_integer(input(prompt), minimum, maximum)
        except ValueError as error:
            print(f'Error: {error}')


def read_text(prompt: str = 'Enter text: ') -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print('Error: text must not be empty or consist of spaces only!')


def read_choice(prompt: str, options: tuple[str, ...]) -> str:
    allowed = '/'.join(options)
    while True:
        value = input(f'{prompt} ({allowed}): ').strip().lower()
        if value in options:
            return value
        print(f'Error: value must be one of: {allowed}.')


def parse_date(text: str) -> date:
    text = text.strip()
    if len(text) != 10:
        raise ValueError
    return datetime.strptime(text, DATE_FORMAT).date()


def format_date(value: date) -> str:
    return value.strftime(DATE_FORMAT)


def read_date(prompt: str = 'Date (dd.mm.yyyy): ') -> date:
    while True:
        try:
            return parse_date(input(prompt))
        except ValueError:
            print('Error: invalid date. Use dd.mm.yyyy, for example 05.09.2026.')


def show_numbered(items: list, empty_message: str = 'Nothing to show.', formatter: Callable = str) -> None:
    if not items:
        print(empty_message)
        return
    for index, item in enumerate(items, start=1):
        print(f'{index}. {formatter(item)}')


def run_menu(title: str, options: list[MenuOption], on_exit: Callable[[], None] | None = None) -> None:
    exit_number = len(options) + 1
    while True:
        print(f'\n--- {title} ---')
        for number, (label, _) in enumerate(options, start=1):
            print(f'{number}. {label}')
        print(f'{exit_number}. Exit')
        choice = input(f'Select an option (1-{exit_number}): ').strip()

        try:
            number = parse_integer(choice, 1, exit_number)
        except ValueError:
            print(f'\n[Error]: Invalid choice. Please enter a number between 1 and {exit_number}.')
            continue

        if number == exit_number:
            if on_exit:
                on_exit()
            print('\nProgram exiting. Goodbye!')
            return

        label, action = options[number - 1]
        print(f'\n--- [Running: {number}. {label}] ---')
        action()

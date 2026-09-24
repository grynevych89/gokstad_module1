from constants import DATE_FORMAT, TIME_FORMAT
from datetime import date, datetime, time


def read_integer(prompt: str, minimum: int | None = None, maximum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Error: please enter a valid integer.')
            continue
        if minimum is not None and value < minimum:
            print(f'Error: value must be at least {minimum}.')
            continue
        if maximum is not None and value > maximum:
            print(f'Error: value must be at most {maximum}.')
            continue
        return value


def read_text(prompt: str = 'Enter text: ') -> str:
    while True:
        text_example = input(prompt)
        if not text_example.strip():
            print('Error: text must not be empty or consist of spaces only!')
            continue
        return text_example


def confirm(prompt: str) -> bool:
    return input(f'{prompt} (y/n): ').strip().lower() == 'y'


def parse_date(text: str) -> date:
    text = text.strip()
    if len(text) != 10:
        raise ValueError
    return datetime.strptime(text, DATE_FORMAT).date()


def parse_time(text: str) -> time:
    text = text.strip()
    if len(text) != 5:
        raise ValueError
    return datetime.strptime(text, TIME_FORMAT).time()


def format_date(value: date) -> str:
    return value.strftime(DATE_FORMAT)


def read_date(prompt: str = 'Date (dd.mm.yyyy): ') -> date:
    while True:
        try:
            return parse_date(input(prompt))
        except ValueError:
            print('Error: invalid date. Use dd.mm.yyyy, for example 05.09.2026.')


def read_time(prompt: str = 'Start time (hh:mm): ') -> time:
    while True:
        try:
            return parse_time(input(prompt))
        except ValueError:
            print('Error: invalid time. Use hh:mm, for example 18:30.')

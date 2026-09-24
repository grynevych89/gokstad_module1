from datetime import date, datetime, timedelta, time
from constants import TIME_FORMAT
from helpers import format_date, parse_date, read_date, read_integer, run_menu, show_numbered


def parse_time(text: str) -> time:
    text = text.strip()
    if len(text) != 5:
        raise ValueError
    return datetime.strptime(text, TIME_FORMAT).time()


def read_time(prompt: str = 'Start time (hh:mm): ') -> time:
    while True:
        try:
            return parse_time(input(prompt))
        except ValueError:
            print('Error: invalid time. Use hh:mm, for example 18:30.')


def read_date_list() -> list[date]:
    dates: list[date] = []
    while True:
        text = input('Date (empty line to finish): ').strip()
        if not text:
            if dates:
                return dates
            print('Error: at least one date is required.')
            continue
        try:
            dates.append(parse_date(text))
        except ValueError:
            print('Error: invalid date. Use dd.mm.yyyy.')


def end_time(session_date: date, start: time, minutes: int) -> tuple[time, int]:
    start_point = datetime.combine(session_date, start)
    end_point = start_point + timedelta(minutes=minutes)
    return end_point.time(), (end_point.date() - session_date).days


def days_between(first: date, second: date) -> int:
    return abs((second - first).days)


def sort_dates(dates: list[date]) -> list[date]:
    return sorted(dates)


def plan_session() -> None:
    session_date = read_date('Session date (dd.mm.yyyy): ')
    start = read_time('Start time (hh:mm): ')
    minutes = read_integer('Duration in minutes: ', 1)
    finish, next_day = end_time(session_date, start, minutes)
    suffix = ' (next day)' if next_day else ''
    print(f'{format_date(session_date)} | {start.strftime(TIME_FORMAT)} - '
          f'{finish.strftime(TIME_FORMAT)}{suffix} | {minutes} min')


def count_days() -> None:
    first = read_date('First date (dd.mm.yyyy): ')
    second = read_date('Second date (dd.mm.yyyy): ')
    print(f'Days between: {days_between(first, second)}')


def show_sorted_dates() -> None:
    show_numbered(sort_dates(read_date_list()), formatter=format_date)


def check_date() -> None:
    value = read_date('Date to check (dd.mm.yyyy): ')
    print(f'Valid date: {format_date(value)}')


def main() -> None:
    run_menu('SESSION PLANNER', [
        ('Check a date (dd.mm.yyyy)', check_date),
        ('Plan a study session (end time)', plan_session),
        ('Count days between two dates', count_days),
        ('Sort a list of dates', show_sorted_dates),
    ])


if __name__ == '__main__':
    main()
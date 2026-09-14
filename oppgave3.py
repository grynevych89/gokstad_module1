from datetime import date, datetime, timedelta, time
from constants import TIME_FORMAT
from helpers import read_integer, read_date, format_date, parse_date, read_time


def read_date_list():
    dates = []
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


def plan_session():
    session_date = read_date('Session date (dd.mm.yyyy): ')
    start = read_time('Start time (hh:mm): ')
    minutes = read_integer('Duration in minutes: ', 1)
    finish, next_day = end_time(session_date, start, minutes)
    suffix = ' (next day)' if next_day else ''
    print(f'{format_date(session_date)} | {start.strftime(TIME_FORMAT)} - '
          f'{finish.strftime(TIME_FORMAT)}{suffix} | {minutes} min')


def count_days():
    first = read_date('First date (dd.mm.yyyy): ')
    second = read_date('Second date (dd.mm.yyyy): ')
    print(f'Days between: {days_between(first, second)}')


def show_sorted_dates():
    ordered = sort_dates(read_date_list())
    for i, value in enumerate(ordered, start=1):
        print(f'{i}. {format_date(value)}')


def check_date():
    value = read_date('Date to check (dd.mm.yyyy): ')
    print(f'Valid date: {format_date(value)}')


def main():
    while True:
        print('\n--- SESSION PLANNER ---')
        print('1. Check a date (dd.mm.yyyy)')
        print('2. Plan a study session (end time)')
        print('3. Count days between two dates')
        print('4. Sort a list of dates')
        print('5. Exit')
        choice = input('Select an option (1-5): ').strip()

        if choice == '1':
            print('\n--- [Running: 1. Check a date] ---')
            check_date()
        elif choice == '2':
            print('\n--- [Running: 2. Plan a study session] ---')
            plan_session()
        elif choice == '3':
            print('\n--- [Running: 3. Count days between two dates] ---')
            count_days()
        elif choice == '4':
            print('\n--- [Running: 4. Sort a list of dates] ---')
            show_sorted_dates()
        elif choice == '5':
            print('\nProgram exiting. Goodbye!')
            break
        else:
            print('\n[Error]: Invalid choice. Please enter a number between 1 and 5.')


if __name__ == '__main__':
    main()

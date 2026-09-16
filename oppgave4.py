import csv
from collections import Counter
from operator import itemgetter
from typing import TypedDict

CSV_FILE = 'supporthenvendelser.csv'
REPORT_FILE = 'support-rapport.txt'
REQUIRED_FIELDS = ('id', 'category', 'minutes', 'is_resolved')
WIDTH = 40
TITLE_LINE = '=' * WIDTH
LINE = '-' * WIDTH


class Request(TypedDict):
    id: int
    category: str
    minutes: int
    is_resolved: bool


def parse_integer(field: str, text: str, minimum: int) -> int:
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f'{field} is not an integer: {text}') from None
    if value < minimum:
        raise ValueError(f'{field} must be at least {minimum}: {text}')
    return value


def parse_row(raw_row: dict[str, str]) -> Request:
    row = {key: (value or '').strip() for key, value in raw_row.items()}
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            raise ValueError(f'field {field} is empty or missing')

    is_resolved = row['is_resolved']
    if is_resolved not in ('yes', 'no'):
        raise ValueError(f'is_resolved must be yes or no: {is_resolved}')

    return {
        'id': parse_integer('id', row['id'], 1),
        'category': row['category'],
        'minutes': parse_integer('minutes', row['minutes'], 0),
        'is_resolved': is_resolved == 'yes',
    }


def read_requests(path: str) -> list[Request]:
    requests: list[Request] = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    requests.append(parse_row(row))
                except ValueError as error:
                    print(f'Line {reader.line_num}: skipped - {error}')
    except OSError as error:
        print(f'Error: could not read {path}: {error}')
    except UnicodeDecodeError as error:
        print(f'Error: {path} is not valid UTF-8: {error}')
    except csv.Error as error:
        print(f'Error: could not parse {path}: {error}')
    return requests


def build_report(requests: list[Request]) -> str:
    per_category = Counter(item['category'] for item in requests)
    top_category, top_count = per_category.most_common(1)[0]
    total_minutes = sum(item['minutes'] for item in requests)
    resolved_count = sum(item['is_resolved'] for item in requests)
    unresolved = sorted(
        (item for item in requests if not item['is_resolved']),
        key=itemgetter('minutes'),
        reverse=True,
    )
    unresolved_lines = [
        'id {id} - {category} - {minutes} minutes'.format(**item) for item in unresolved
    ] or ['No unresolved requests']

    lines = [
        'SUPPORT REPORT',
        TITLE_LINE,
        '',
        f'Valid requests: {len(requests)}',
        '',
        'Requests per category',
        LINE,
        *(f'{name}: {count}' for name, count in per_category.most_common()),
        '',
        'Time spent',
        LINE,
        f'Total time: {total_minutes} minutes',
        f'Average time: {total_minutes / len(requests):.1f} minutes',
        '',
        'Status',
        LINE,
        f'Resolved requests: {resolved_count}',
        f'Unresolved requests: {len(unresolved)}',
        '',
        'Category with most requests',
        LINE,
        f'{top_category} ({top_count} requests)',
        '',
        'Unresolved requests sorted by time spent (descending)',
        LINE,
        *unresolved_lines,
    ]
    return '\n'.join(lines) + '\n'


def write_report(path: str, text: str) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    except OSError as error:
        print(f'Error: could not write {path}: {error}')
    else:
        print(f'Report written to {path}')


def main() -> None:
    requests = read_requests(CSV_FILE)
    if not requests:
        print('No valid rows found, report was not generated.')
        return
    write_report(REPORT_FILE, build_report(requests))


if __name__ == '__main__':
    main()


# def sum_resolved_minutes(requests: list[dict[str, str | int]]) -> int:
#     total = 0
#     for request in requests:
#         if request['is_resolved'] == 'yes':
#             total += request['minutes']
#     return total
#
#
# requests = [
#     {'id': 1, 'category': 'innlogging', 'minutes': 18, 'is_resolved': 'yes'},
#     {'id': 2, 'category': 'programvare', 'minutes': 42, 'is_resolved': 'no'},
#     {'id': 3, 'category': 'nettverk', 'minutes': 27, 'is_resolved': 'yes'},
# ]
# print(sum_resolved_minutes(requests))  # 45

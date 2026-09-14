# Arbeidskrav 1 – Python

**Student:** Mykola Grynevych

## How to run

Developed and tested with Python 3.14.7. Requires Python 3.10 or newer.
Run from the project folder:

```bash
python3 oppgave1.py
python3 oppgave2.py
python3 oppgave3.py
```

## File structure

- `oppgave1.py` – Oppgave 1, basic program flow (1.1–1.4)
- `oppgave2.py` – Oppgave 2, data structures and data handling
- `oppgave3.py` – Oppgave 3, functions and documentation
- `helpers.py` – shared input and parsing helpers used by several tasks
- `constants.py` – date and time format strings
- `data.py` – example sessions with a TypedDict (in-memory "database")
- `README.md` – this file

### File naming

The assignment lists the files as `oppgave-1.py` … `oppgave-5.py`. I have
deliberately named them `oppgave1.py` … `oppgave5.py` instead: a hyphen is not
allowed in Python module names (`import oppgave-1` is a syntax error), and
PEP 8 requires `snake_case` for modules. Without the hyphen the files can be
imported and tested like any other module.

### Shared modules

The assignment says all subtasks of a main task should be in the same file.
The task logic follows that rule. Three things are placed outside:

- `helpers.py` – input and parsing functions that more than one task needs:
  `read_integer()`, `read_text()`, `parse_date()`, `parse_time()`,
  `format_date()`, `read_date()`, `read_time()`. Duplicating them across task
  files would violate the DRY principle. Helpers used by only one task were not
  extracted.
- `constants.py` – `DATE_FORMAT` and `TIME_FORMAT`, so that the formats are
  defined in one place.
- `data.py` – the example sessions, kept separate from the program logic as an
  in-memory "database". This makes it easy to swap in real storage later.

Splitting the code across modules also demonstrates working with imports.

## Oppgave 1 – Basic program flow

`oppgave1.py`

- 1.1 – reads sessions and minutes per session via `read_integer(minimum=1)`,
  converts the total with `// 60` and `% 60`.
- 1.2 – reads text via `read_text()`, prints lengths with/without whitespace,
  lowercase, reversed, and a case-insensitive check for `python`.
- 1.3 – reads start and end as integers, iterates `range(start, end + 1)` and
  prints even numbers, numbers divisible by 3, and the sum.
- 1.4 – menu loop; any input other than `1`–`4` shows an error and re-displays
  the menu.

**Deliberate deviation in 1.3:** the assignment asks for an error message when
the start value is greater than the end value. Instead, the program swaps the
two values and continues. From the user's point of view the interval 10–1 is
the same as 1–10, so asking the user to re-enter the same numbers in a
different order adds friction without adding safety. Both boundaries are still
validated as integers.

## Oppgave 2 – Data structures and data handling

`oppgave2.py`, with data in `data.py` and shared input helpers in `helpers.py`.

### Choice of data structure

Sessions are stored as a `list` of `dict` objects with the fields `topic`,
`duration_minutes` and `status`. The shape is described by a `TypedDict`
(`Session`) in `data.py`. I chose `dict` over `tuple` because the fields are
accessed by name instead of by index, a session can be updated in place
(e.g. status change), and new fields can be added later without touching
existing code. A `list` keeps the registration order and makes filtering,
searching and sorting straightforward.

### Structure

`oppgave2.py` contains the menu and all task-specific functions: register,
show all, show completed, search, sort by duration, statistics.

### Validation

Empty topic, non-positive or non-integer duration, and any status other than
`planned` / `completed` are rejected with a message and the user is asked
again. Empty search or filter results print a clear message instead of nothing.
Invalid menu choices show an error and re-display the menu.

## Oppgave 3 – Functions and documentation

`oppgave3.py`, with parsing helpers in `helpers.py` and formats in
`constants.py`.

### Standard library

The task is solved with the `datetime` module from the Python standard
library:

- Documentation title: *datetime — Basic date and time types*
- URL: https://docs.python.org/3/library/datetime.html

`datetime.strptime()` is used for parsing, `date` and `time` objects for
values, `timedelta` for arithmetic, and `datetime.combine()` to add minutes to
a start time.

### Functions

All calculation logic lives in functions that return values; the menu
functions only read input and print the returned results.

| Function | Location | Parameters | Returns |
|---|---|---|---|
| `parse_date(text)` | `helpers.py` | `str` in `dd.mm.yyyy` | `date`, or raises `ValueError` |
| `parse_time(text)` | `helpers.py` | `str` in `hh:mm` | `time`, or raises `ValueError` |
| `end_time(session_date, start, minutes)` | `oppgave3.py` | `date`, `time`, `int` | `tuple[time, int]` – end time and number of days rolled over |
| `days_between(first, second)` | `oppgave3.py` | `date`, `date` | `int`, always non-negative |
| `sort_dates(dates)` | `oppgave3.py` | `list[date]` | new `list[date]`, chronological |

`parse_date()` and `parse_time()` are placed in `helpers.py` because Oppgave 5
needs the same date validation. `oppgave3.py` imports and uses them.

Both parsers check the exact string length before calling `strptime()`, since
`%d`, `%m` and `%H` would otherwise accept single-digit values such as
`5.9.2026`, which is not the required `dd.mm.yyyy` format.

### Validation

Invalid date format, non-existent dates (e.g. `31.02.2026`), invalid time, and
non-positive or non-integer duration are all rejected with an explanatory
message and the user is asked again. The date list requires at least one valid
date before it can be sorted.

### Test cases

| # | Input | Expected result | Result |
|---|---|---|---|
| 1 | `parse_date('05.09.2026')` | `date(2026, 9, 5)` | OK |
| 2 | `parse_date('29.02.2024')` (leap year) | `date(2024, 2, 29)` | OK |
| 3 | `parse_date('31.02.2026')` (non-existent date) | `ValueError` → error message, asked again | OK |
| 4 | `parse_date('5.9.2026')` (single-digit day/month) | `ValueError` → error message, asked again | OK |
| 5 | `parse_date('05/09/2026')` (wrong separator) | `ValueError` → error message, asked again | OK |
| 6 | `parse_date('abc')` | `ValueError` → error message, asked again | OK |
| 7 | `end_time(05.09.2026, 18:30, 90)` | `20:00`, same day | OK |
| 8 | `end_time(05.09.2026, 23:30, 60)` | `00:30`, next day | OK |
| 9 | Duration `0` / `-5` / `abc` | Rejected by `read_integer(minimum=1)`, asked again | OK |
| 10 | Start time `25:00` / `8:30` | `ValueError` → error message, asked again | OK |
| 11 | `days_between(01.09.2026, 25.09.2026)` | `24` | OK |
| 12 | `days_between(25.09.2026, 01.09.2026)` (reversed) | `24` (always positive) | OK |
| 13 | `sort_dates([25.09.2026, 01.09.2026, 14.09.2026])` | `[01.09.2026, 14.09.2026, 25.09.2026]` | OK |
| 14 | Date list: empty line as first input | Error message, at least one date required | OK |

## AI Documentation

I have used AI (Claude) to a limited extent while working on this arbeidskrav.
The main uses were language-related:

- Translating the assignment text from Norwegian into my native language, so that
  I could understand the requirements correctly.
- Translating and proofreading this `README.md`, which I drafted in my native
  language and then rendered into English.

Neither of these influenced the design or the logic of my solution, and they are
therefore not documented as individual prompts.

The exchanges that had a direct influence on the code are documented below.

### Prompt 1 — Oppgave 1.1

**Prompt:** "formula 1.1?" (originally asked in my native language: «формула 1.1?»
— asking for the formula used to convert total minutes into hours and minutes in
Oppgave 1.1)

**Response:**

    total_minutes = sessions * minutes_per_session
    hours   = total_minutes // 60
    minutes = total_minutes %  60

    Check against the example: 5 × 45 = 225 → 225 // 60 = 3, 225 % 60 = 45
    → "3 timer og 45 minutter".

**How it was used and quality assured:** This is standard integer division and
modulo arithmetic. I used the same principle in `oppgave1.py`, written in my own
code. I verified it against the example given in the assignment text
(5 sessions × 45 minutes = 225 minutes → 3 hours and 45 minutes)
and against the official documentation for the `//` and `%` operators:
https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations

### Oppgave 2

No AI was used for Oppgave 2.

### Prompt 2 — Oppgave 3, code review

**Prompt:** "check task 3" (originally: «проверь выполнение задания 3»), with
`oppgave3.py` and `constants.py` attached. I wrote the solution myself first
and asked for a review against the assignment requirements.

**Response (summary of the points I acted on):**

1. `end_time()` combined the start time with `date.today()` instead of the
   session date read from the user, so the "next day" flag was computed from
   the wrong date. Suggested passing `session_date` as a parameter.
2. `strptime` with `%d.%m.%Y` accepts `5.9.2026`, which is not strictly
   `dd.mm.yyyy`. Suggested checking `len(text) == 10` before parsing. I applied
   the same idea to `parse_time()` (`len(text) == 5`).
3. Type hints were missing on the Oppgave 3 functions while present in
   `helpers.py`. Suggested adding them for consistency.

**How it was used and quality assured:** I implemented the three changes
myself. Point 1 I verified by planning a session on a date other than today
with a start time near midnight and checking the day rollover. Point 2 I
verified by running the invalid inputs in test cases 4 and 10 above. Point 3
I checked against the `datetime` documentation for the correct type names.

### Other sources

Apart from the above, I did not use AI to write, design or debug the solution.
The sources I used were:

- The official Python documentation: https://docs.python.org/3/
- General web searches and Stack Overflow for syntax lookups
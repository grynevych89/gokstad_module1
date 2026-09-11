# Arbeidskrav 1 – Python

**Student:** Mykola Grynevych

## How to run

Developed and tested with Python 3.14.7. Requires Python 3.10 or newer.
Run from the project folder:

```bash
python3 oppgave1.py
python3 oppgave2.py
```

## File structure

- `oppgave1.py` – Oppgave 1, basic program flow (1.1–1.4)
- `oppgave2.py` – Oppgave 2, data structures and data handling
- `helpers.py` – shared input helpers used by both tasks
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
The task logic follows that rule. Two things are placed outside:

- `helpers.py` – `read_integer()` and `read_text()`, which were moved out of
  `oppgave1.py` because Oppgave 2 needs the same validated input. Duplicating
  them would violate the DRY principle. Helpers used by only one task were not
  extracted.
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

## Oppgave 2 – Data structures and data handling

`oppgave2.py`, with data in `data.py` and shared input helpers in `helpers.py`.

### Choice of data structure

Sessions are stored as a `list` of `dict` objects with the fields `topic`,
`duration_minutes` and `status`. The shape is described by a `TypedDict`
(`Session`) in `data.py`. I chose `dict` over `tuple` because the fields are
accessed by name instead of by index, a session can be updated in place (e.g. status change), and new fields can be
added later without touching
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

## AI Documentation

I have used AI (Claude) to a limited extent while working on this arbeidskrav.
The main uses were language-related:

- Translating the assignment text from Norwegian into my native language, so that
  I could understand the requirements correctly.
- Translating and proofreading this `README.md`, which I drafted in my native
  language and then rendered into English.

Neither of these influenced the design or the logic of my solution, and they are
therefore not documented as individual prompts.

One exchange had a direct, although minimal, influence on the code, and is
documented here.

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

### Other sources

Apart from the above, I did not use AI to write, design or debug the solution.
The sources I used were:

- The official Python documentation: https://docs.python.org/3/
- General web searches and Stack Overflow for syntax lookups

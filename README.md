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
modulo arithmetic. I used the same principle in `oppgave-1.py`, written in my own
code. I verified it against the example given in the assignment text
(5 sessions × 45 minutes = 225 minutes → 3 hours and 45 minutes) and against the
official documentation for the `//` and `%` operators:
https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations

### Other sources

Apart from the above, I did not use AI to write, design or debug the solution.
The sources I used were:

- The official Python documentation: https://docs.python.org/3/
- General web searches and Stack Overflow for syntax lookups
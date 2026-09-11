from typing import TypedDict


class Session(TypedDict):
    topic: str
    duration_minutes: int
    status: str


sessions: list[Session] = [
    {'topic': 'Lists and dictionaries', 'duration_minutes': 60, 'status': 'completed'},
    {'topic': 'Python basics', 'duration_minutes': 45, 'status': 'completed'},
    {'topic': 'Functions in Python', 'duration_minutes': 30, 'status': 'planned'},
    {'topic': 'Error handling', 'duration_minutes': 90, 'status': 'completed'},
    {'topic': 'Git and GitHub', 'duration_minutes': 25, 'status': 'planned'},
]

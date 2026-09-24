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


sample_activities: list[dict] = [
    {'title': 'Morning run', 'category': 'sport', 'date': '28.09.2026', 'estimated_minutes': 40, 'status': 'planned'},
    {'title': 'Read Python docs', 'category': 'study', 'date': '25.09.2026', 'estimated_minutes': 60, 'status': 'completed'},
    {'title': 'Walk the dog', 'category': 'home', 'date': '26.09.2026', 'estimated_minutes': 30, 'status': 'completed'},
    {'title': 'Git and GitHub', 'category': 'study', 'date': '02.10.2026', 'estimated_minutes': 90, 'status': 'planned'},
    {'title': 'Swimming', 'category': 'sport', 'date': '30.09.2026', 'estimated_minutes': 45, 'status': 'planned'},
    {'title': 'Clean the kitchen', 'category': 'home', 'date': '24.09.2026', 'estimated_minutes': 20, 'status': 'completed'},
]
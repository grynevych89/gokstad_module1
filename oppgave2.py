from constants import STATUSES
from data import Session, sessions
from helpers import read_choice, read_integer, read_text, run_menu, show_numbered


def format_session(session: Session) -> str:
    return f'{session["topic"]} | {session["duration_minutes"]} min | {session["status"]}'


def show_sessions(items: list[Session], empty_message: str = 'No sessions to show.') -> None:
    show_numbered(items, empty_message, format_session)


def register_session(items: list[Session]) -> None:
    items.append({
        'topic': read_text('Topic: '),
        'duration_minutes': read_integer('Duration in minutes: ', minimum=1),
        'status': read_choice('Status', STATUSES),
    })
    print('Session registered.')


def completed_sessions(items: list[Session]) -> list[Session]:
    return [s for s in items if s['status'] == 'completed']


def show_completed(items: list[Session]) -> None:
    show_sessions(completed_sessions(items), 'No completed sessions.')


def search_topic(items: list[Session]) -> None:
    keyword = read_text('Search word: ').lower()
    matches = [s for s in items if keyword in s['topic'].lower()]
    show_sessions(matches, f'No matches for {keyword!r}.')


def sort_by_duration(items: list[Session]) -> None:
    show_sessions(sorted(items, key=lambda s: s['duration_minutes'], reverse=True))


def show_statistics(items: list[Session]) -> None:
    completed = completed_sessions(items)
    if not completed:
        print('No completed sessions to calculate.')
        return
    total = sum(s['duration_minutes'] for s in completed)
    print(f'Completed sessions: {len(completed)}')
    print(f'Total duration: {total} min')
    print(f'Average duration: {total / len(completed):.1f} min')


def main() -> None:
    items = sessions
    run_menu('STUDY SESSIONS', [
        ('Register a study session', lambda: register_session(items)),
        ('Show all sessions', lambda: show_sessions(items, 'No sessions registered.')),
        ('Show only completed sessions', lambda: show_completed(items)),
        ('Search for a word in the topic', lambda: search_topic(items)),
        ('Sort sessions by duration (longest first)', lambda: sort_by_duration(items)),
        ('Show total and average duration (completed)', lambda: show_statistics(items)),
    ])


if __name__ == '__main__':
    main()
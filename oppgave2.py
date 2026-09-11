from data import sessions
from helpers import read_integer


# Helpers
def print_session(session, index=None):
    prefix = f'{index}. ' if index is not None else '- '
    print(f'{prefix}{session["topic"]} | '
          f'{session["duration_minutes"]} min | {session["status"]}')


def show_sessions(items, empty_message='No sessions to show.'):
    if not items:
        print(empty_message)
        return
    for i, session in enumerate(items, start=1):
        print_session(session, i)


def register_session():
    topic = input('Topic: ').strip()
    while not topic:
        print('Topic cannot be empty.')
        topic = input('Topic: ').strip()

    duration = read_integer('Duration in minutes: ', minimum=1)

    status = input('Status (planned/completed): ').strip().lower()
    while status not in ('planned', 'completed'):
        print('Status must be \'planned\' or \'completed\'.')
        status = input('Status (planned/completed): ').strip().lower()

    sessions.append({
        'topic': topic,
        'duration_minutes': duration,
        'status': status,
    })
    print('Session registered.')


def show_completed():
    completed = [s for s in sessions if s['status'] == 'completed']
    show_sessions(completed, 'No completed sessions.')


def search_topic():
    keyword = input('Search word: ').strip().lower()
    if not keyword:
        print('Search word cannot be empty.')
        return
    matches = [s for s in sessions if keyword in s['topic'].lower()]
    show_sessions(matches, f'No matches for {keyword!r}.')


def sort_by_duration():
    ordered = sorted(sessions, key=lambda s: s['duration_minutes'], reverse=True)
    show_sessions(ordered)


def show_statistics():
    completed = [s for s in sessions if s['status'] == 'completed']
    if not completed:
        print('No completed sessions to calculate.')
        return
    total = sum(s['duration_minutes'] for s in completed)
    average = total / len(completed)
    print(f'Completed sessions: {len(completed)}')
    print(f'Total duration: {total} min')
    print(f'Average duration: {average:.1f} min')


def main():
    while True:
        print('\n--- STUDY SESSIONS ---')
        print('1. Register a study session')
        print('2. Show all sessions')
        print('3. Show only completed sessions')
        print('4. Search for a word in the topic')
        print('5. Sort sessions by duration (longest first)')
        print('6. Show total and average duration (completed)')
        print('7. Exit')
        choice = input('Select an option (1-7): ').strip()

        if choice == '1':
            print('\n--- [Running: 1. Register a study session] ---')
            register_session()
        elif choice == '2':
            print('\n--- [Running: 2. Show all sessions] ---')
            show_sessions(sessions, '\n--- [No sessions registered.] ---')
        elif choice == '3':
            print('\n--- [Running: 3. Show only completed sessions] ---')
            show_completed()
        elif choice == '4':
            print('\n--- [Running: 4. Search for a word in the topic] ---')
            search_topic()
        elif choice == '5':
            print('\n--- [Running: 5. Sort sessions by duration] ---')
            sort_by_duration()
        elif choice == '6':
            print('\n--- [Running: 6. Total and average duration] ---')
            show_statistics()
        elif choice == '7':
            print('\nProgram exiting. Goodbye!')
            break
        else:
            print('\n[Error]: Invalid choice. Please enter a number between 1 and 7.')


if __name__ == '__main__':
    main()

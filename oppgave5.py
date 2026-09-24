import json
from datetime import date
from constants import STATUSES
from data import sample_activities
from helpers import (
    format_date, parse_date, read_choice, read_date,
    read_integer, read_text, run_menu, show_numbered,
)

DATA_FILE = 'activities.json'


def confirm(prompt: str) -> bool:
    return input(f'{prompt} (y/n): ').strip().lower() == 'y'


class Activity:
    def __init__(self, title: str, category: str, activity_date: date,
                 estimated_minutes: int, status: str = 'planned'):
        self.title = title
        self.category = category
        self.date = activity_date
        self.estimated_minutes = estimated_minutes
        self.status = status

    def mark_completed(self) -> bool:
        if self.status == 'completed':
            return False
        self.status = 'completed'
        return True

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'category': self.category,
            'date': format_date(self.date),
            'estimated_minutes': self.estimated_minutes,
            'status': self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        title = str(data['title']).strip()
        category = str(data['category']).strip()
        minutes = data['estimated_minutes']
        status = data['status']
        if not title or not category:
            raise ValueError('title and category must not be empty')
        if not isinstance(minutes, int) or minutes < 1:
            raise ValueError(f'estimated_minutes must be a positive integer: {minutes}')
        if status not in STATUSES:
            raise ValueError(f'status must be planned or completed: {status}')
        return cls(title, category, parse_date(str(data['date'])), minutes, status)

    def __str__(self) -> str:
        return (f'{self.title} | {self.category} | {format_date(self.date)} | '
                f'{self.estimated_minutes} min | {self.status}')


def show_activities(items: list[Activity], empty_message: str = 'No activities to show.') -> None:
    show_numbered(items, empty_message)


def register_activity(activities: list[Activity]) -> None:
    activities.append(Activity(
        read_text('Title: '),
        read_text('Category: '),
        read_date('Date (dd.mm.yyyy): '),
        read_integer('Estimated minutes: ', minimum=1),
        read_choice('Status', STATUSES),
    ))
    print('Activity registered.')


def search_activities(activities: list[Activity]) -> None:
    keyword = read_text('Search word (title or category): ').lower()
    matches = [
        activity for activity in activities
        if keyword in activity.title.lower() or keyword in activity.category.lower()
    ]
    show_activities(matches, f'No matches for {keyword!r}.')


def filter_by_status(activities: list[Activity]) -> None:
    status = read_choice('Show status', STATUSES)
    matches = [activity for activity in activities if activity.status == status]
    show_activities(matches, f'No {status} activities.')


def sort_activities(activities: list[Activity]) -> None:
    choice = read_choice('Sort by', ('date', 'duration'))
    if choice == 'date':
        ordered = sorted(activities, key=lambda activity: activity.date)
    else:
        ordered = sorted(activities, key=lambda activity: activity.estimated_minutes, reverse=True)
    show_activities(ordered)


def complete_activity(activities: list[Activity]) -> None:
    planned = [activity for activity in activities if activity.status == 'planned']
    if not planned:
        print('No planned activities to complete.')
        return
    show_activities(planned)
    number = read_integer('Number to mark as completed: ', 1, len(planned))
    activity = planned[number - 1]
    activity.mark_completed()
    print(f'Marked as completed: {activity.title}')


def show_statistics(activities: list[Activity]) -> None:
    total_minutes = sum(activity.estimated_minutes for activity in activities)
    completed = sum(activity.status == 'completed' for activity in activities)
    print(f'Activities: {len(activities)}')
    print(f'Total estimated time: {total_minutes} min')
    print(f'Completed: {completed}')


def save_activities(activities: list[Activity], path: str = DATA_FILE) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump([activity.to_dict() for activity in activities], file, indent=2, ensure_ascii=False)
    except OSError as error:
        print(f'Error: could not write {path}: {error}')
    else:
        print(f'Saved {len(activities)} activities to {path}.')


def load_activities(path: str = DATA_FILE) -> list[Activity]:
    try:
        with open(path, encoding='utf-8') as file:
            raw_items = json.load(file)
    except FileNotFoundError:
        print(f'No data file {path} found, starting with an empty list.')
        return []
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f'Error: could not read {path}: {error}. Starting with an empty list.')
        return []
    if not isinstance(raw_items, list):
        print(f'Error: {path} does not contain a list. Starting with an empty list.')
        return []

    activities = []
    for index, item in enumerate(raw_items, start=1):
        try:
            activities.append(Activity.from_dict(item))
        except (KeyError, TypeError, ValueError) as error:
            print(f'Entry {index}: skipped - {error}')
    print(f'Loaded {len(activities)} activities from {path}.')
    return activities


def load_sample_activities() -> list[Activity]:
    activities = [Activity.from_dict(item) for item in sample_activities]
    print(f'Loaded {len(activities)} sample activities.')
    return activities


def merge_activities(activities: list[Activity], new_items: list[Activity]) -> None:
    if not new_items:
        return
    if activities:
        choice = read_choice(f'You already have {len(activities)} activities', ('replace', 'add'))
        if choice == 'replace':
            activities.clear()
    activities.extend(new_items)
    print(f'Activities now: {len(activities)}')


def clear_activities(activities: list[Activity]) -> None:
    if not activities:
        print('No activities to clear.')
        return
    if not confirm(f'Delete all {len(activities)} activities?'):
        print('Cancelled.')
        return
    activities.clear()
    print('All activities deleted.')


def main() -> None:
    activities = load_activities()

    def on_exit() -> None:
        if confirm('Save changes before exit?'):
            save_activities(activities)

    run_menu('ACTIVITY PLANNER', [
        ('Register an activity', lambda: register_activity(activities)),
        ('Show all activities', lambda: show_activities(activities, 'No activities registered.')),
        ('Search by title or category', lambda: search_activities(activities)),
        ('Filter by status', lambda: filter_by_status(activities)),
        ('Sort by date or duration', lambda: sort_activities(activities)),
        ('Mark an activity as completed', lambda: complete_activity(activities)),
        ('Show statistics', lambda: show_statistics(activities)),
        ('Save activities to file', lambda: save_activities(activities)),
        ('Load activities from file', lambda: merge_activities(activities, load_activities())),
        ('Load example data', lambda: merge_activities(activities, load_sample_activities())),
        ('Clear all activities', lambda: clear_activities(activities)),
    ], on_exit)


if __name__ == '__main__':
    main()
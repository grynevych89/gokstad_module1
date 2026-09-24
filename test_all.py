import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, time
from unittest.mock import patch

import helpers
import oppgave1
import oppgave2
import oppgave3
import oppgave4
import oppgave5
from oppgave5 import Activity


def run_with_input(function, inputs, *args, **kwargs):
    output = io.StringIO()
    with patch('builtins.input', side_effect=inputs), redirect_stdout(output):
        result = function(*args, **kwargs)
    return result, output.getvalue()


class HelpersTest(unittest.TestCase):
    def test_parse_integer_valid(self):
        self.assertEqual(helpers.parse_integer('42'), 42)
        self.assertEqual(helpers.parse_integer('5', minimum=1, maximum=10), 5)

    def test_parse_integer_invalid(self):
        with self.assertRaises(ValueError):
            helpers.parse_integer('abc')
        with self.assertRaises(ValueError):
            helpers.parse_integer('0', minimum=1)
        with self.assertRaises(ValueError):
            helpers.parse_integer('11', maximum=10)

    def test_read_integer_retries_until_valid(self):
        value, output = run_with_input(helpers.read_integer, ['abc', '-1', '7'], 'N: ', 1)
        self.assertEqual(value, 7)
        self.assertEqual(output.count('Error'), 2)

    def test_read_text_rejects_blank(self):
        value, output = run_with_input(helpers.read_text, ['', '   ', 'hello'])
        self.assertEqual(value, 'hello')
        self.assertEqual(output.count('Error'), 2)

    def test_read_choice(self):
        value, output = run_with_input(helpers.read_choice, ['done', 'PLANNED'], 'Status', ('planned', 'completed'))
        self.assertEqual(value, 'planned')
        self.assertIn('Error', output)

    def test_parse_date_valid(self):
        self.assertEqual(helpers.parse_date('05.09.2026'), date(2026, 9, 5))
        self.assertEqual(helpers.parse_date('29.02.2024'), date(2024, 2, 29))

    def test_parse_date_invalid(self):
        for text in ['31.02.2026', '5.9.2026', '05/09/2026', 'abc', '']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                helpers.parse_date(text)

    def test_format_date_roundtrip(self):
        self.assertEqual(helpers.format_date(date(2026, 9, 5)), '05.09.2026')

    def test_show_numbered_empty_and_formatter(self):
        _, output = run_with_input(helpers.show_numbered, [], [], 'nothing')
        self.assertEqual(output.strip(), 'nothing')
        _, output = run_with_input(helpers.show_numbered, [], [3, 4], formatter=lambda n: n * 2)
        self.assertEqual(output, '1. 6\n2. 8\n')

    def test_run_menu_invalid_then_action_then_exit(self):
        calls = []
        options = [('Do it', lambda: calls.append('done'))]
        _, output = run_with_input(helpers.run_menu, ['9', 'x', '1', '2'], 'T', options)
        self.assertEqual(calls, ['done'])
        self.assertEqual(output.count('[Error]'), 2)
        self.assertIn('Goodbye', output)


class Oppgave1Test(unittest.TestCase):
    def test_time_spent(self):
        _, output = run_with_input(oppgave1.calculation_of_time_spent, ['5', '45'])
        self.assertIn('3 hours, 45 minutes', output)

    def test_time_spent_rejects_zero_and_text(self):
        _, output = run_with_input(oppgave1.calculation_of_time_spent, ['0', 'abc', '2', '30'])
        self.assertEqual(output.count('Error'), 2)
        self.assertIn('1 hours, 0 minutes', output)

    def test_text_analysis(self):
        _, output = run_with_input(oppgave1.text_analysis, ['Hello World!@Python'])
        self.assertIn('Length with spaces: 19', output)
        self.assertIn('Length without spaces: 18', output)
        self.assertIn('Reversed: nohtyP@!dlroW olleH', output)
        self.assertIn('Contains "python": True', output)

    def test_numeric_range(self):
        _, output = run_with_input(oppgave1.numeric_range_analysis, ['1', '10'])
        self.assertIn('Even numbers: [2, 4, 6, 8, 10]', output)
        self.assertIn('Divisible by 3: [3, 6, 9]', output)
        self.assertIn('Sum: 55', output)

    def test_numeric_range_swaps_reversed_bounds(self):
        _, output = run_with_input(oppgave1.numeric_range_analysis, ['10', '1'])
        self.assertIn('Sum: 55', output)


class Oppgave2Test(unittest.TestCase):
    def setUp(self):
        self.items = [
            {'topic': 'Python basics', 'duration_minutes': 45, 'status': 'completed'},
            {'topic': 'Git', 'duration_minutes': 25, 'status': 'planned'},
            {'topic': 'Python testing', 'duration_minutes': 60, 'status': 'completed'},
        ]

    def test_register_with_validation(self):
        _, output = run_with_input(
            oppgave2.register_session, ['', 'Decorators', '-5', '40', 'done', 'completed'], self.items
        )
        self.assertEqual(len(self.items), 4)
        self.assertEqual(self.items[-1], {'topic': 'Decorators', 'duration_minutes': 40, 'status': 'completed'})
        self.assertEqual(output.count('Error'), 3)

    def test_completed_sessions(self):
        self.assertEqual(len(oppgave2.completed_sessions(self.items)), 2)

    def test_search(self):
        _, output = run_with_input(oppgave2.search_topic, ['PYTHON'], self.items)
        self.assertIn('Python basics', output)
        self.assertIn('Python testing', output)
        self.assertNotIn('Git', output)
        _, output = run_with_input(oppgave2.search_topic, ['xyz'], self.items)
        self.assertIn('No matches', output)

    def test_sort_keeps_original_order(self):
        _, output = run_with_input(oppgave2.sort_by_duration, [], self.items)
        self.assertEqual(output.splitlines()[0], '1. Python testing | 60 min | completed')
        self.assertEqual(self.items[0]['topic'], 'Python basics')

    def test_statistics(self):
        _, output = run_with_input(oppgave2.show_statistics, [], self.items)
        self.assertIn('Total duration: 105 min', output)
        self.assertIn('Average duration: 52.5 min', output)
        _, output = run_with_input(oppgave2.show_statistics, [], [])
        self.assertIn('No completed sessions', output)


class Oppgave3Test(unittest.TestCase):
    def test_parse_time(self):
        self.assertEqual(oppgave3.parse_time('18:30'), time(18, 30))
        for text in ['25:00', '8:30', 'abc']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                oppgave3.parse_time(text)

    def test_end_time_same_day(self):
        self.assertEqual(oppgave3.end_time(date(2026, 9, 5), time(18, 30), 90), (time(20, 0), 0))

    def test_end_time_next_day(self):
        self.assertEqual(oppgave3.end_time(date(2026, 9, 5), time(23, 30), 60), (time(0, 30), 1))

    def test_days_between_is_positive(self):
        first, second = date(2026, 9, 1), date(2026, 9, 25)
        self.assertEqual(oppgave3.days_between(first, second), 24)
        self.assertEqual(oppgave3.days_between(second, first), 24)

    def test_sort_dates(self):
        dates = [date(2026, 9, 25), date(2026, 9, 1), date(2026, 9, 14)]
        self.assertEqual(oppgave3.sort_dates(dates), [date(2026, 9, 1), date(2026, 9, 14), date(2026, 9, 25)])
        self.assertEqual(dates[0], date(2026, 9, 25))

    def test_read_date_list_requires_one_valid(self):
        result, output = run_with_input(oppgave3.read_date_list, ['', '5.9.2026', '05.09.2026', ''])
        self.assertEqual(result, [date(2026, 9, 5)])
        self.assertEqual(output.count('Error'), 2)


class Oppgave4Test(unittest.TestCase):
    def test_parse_row_valid(self):
        row = oppgave4.parse_row({'id': '1', 'category': 'innlogging', 'minutes': '18', 'is_resolved': 'yes'})
        self.assertEqual(row, {'id': 1, 'category': 'innlogging', 'minutes': 18, 'is_resolved': True})

    def test_parse_row_invalid(self):
        cases = {
            'empty minutes': {'id': '4', 'category': 'nettverk', 'minutes': '', 'is_resolved': 'no'},
            'id not integer': {'id': 'abc', 'category': 'epost', 'minutes': '10', 'is_resolved': 'yes'},
            'negative id': {'id': '-19', 'category': 'epost', 'minutes': '10', 'is_resolved': 'yes'},
            'negative minutes': {'id': '5', 'category': 'epost', 'minutes': '-3', 'is_resolved': 'yes'},
            'status case': {'id': '6', 'category': 'epost', 'minutes': '15', 'is_resolved': 'Yes'},
            'too many fields': {'id': '7', 'category': 'epost', 'minutes': '15', 'is_resolved': 'yes', None: ['x']},
            'too few fields': {'id': '8', 'category': 'epost', 'minutes': None, 'is_resolved': None},
        }
        for name, raw in cases.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                oppgave4.parse_row(raw)

    def test_read_requests_skips_invalid_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'in.csv')
            with open(path, 'w', encoding='utf-8') as file:
                file.write('id,category,minutes,is_resolved\n1,a,10,yes\nx,a,10,yes\n2,b,20,no\n3,b,5,yes,extra\n')
            _, output = run_with_input(oppgave4.read_requests, [], path)
            requests, _ = run_with_input(oppgave4.read_requests, [], path)
        self.assertEqual([r['id'] for r in requests], [1, 2])
        self.assertIn('Line 3: skipped', output)
        self.assertIn('Line 5: skipped', output)

    def test_read_requests_missing_file(self):
        requests, output = run_with_input(oppgave4.read_requests, [], 'does-not-exist.csv')
        self.assertEqual(requests, [])
        self.assertIn('could not read', output)

    def test_analyze(self):
        requests = [
            {'id': 1, 'category': 'a', 'minutes': 10, 'is_resolved': True},
            {'id': 2, 'category': 'b', 'minutes': 30, 'is_resolved': False},
            {'id': 3, 'category': 'a', 'minutes': 20, 'is_resolved': False},
        ]
        stats = oppgave4.analyze(requests)
        self.assertEqual(stats['total_requests'], 3)
        self.assertEqual(stats['total_minutes'], 60)
        self.assertAlmostEqual(stats['average_minutes'], 20.0)
        self.assertEqual(stats['resolved_count'], 1)
        self.assertEqual([r['id'] for r in stats['unresolved']], [2, 3])
        self.assertEqual((stats['top_category'], stats['top_count']), ('a', 2))

    def test_format_and_write_report(self):
        stats = oppgave4.analyze([{'id': 1, 'category': 'a', 'minutes': 10, 'is_resolved': True}])
        text = oppgave4.format_report(stats)
        self.assertIn('Average time: 10.0 minutes', text)
        self.assertIn('No unresolved requests', text)
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'out.txt')
            run_with_input(oppgave4.write_report, [], path, text)
            run_with_input(oppgave4.write_report, [], path, 'second')
            with open(path, encoding='utf-8') as file:
                self.assertEqual(file.read(), 'second')

    def test_sum_resolved_minutes(self):
        example = [
            {'id': 1, 'category': 'innlogging', 'minutes': 18, 'is_resolved': 'yes'},
            {'id': 2, 'category': 'programvare', 'minutes': 42, 'is_resolved': 'no'},
            {'id': 3, 'category': 'nettverk', 'minutes': 27, 'is_resolved': 'yes'},
        ]
        self.assertEqual(oppgave4.sum_resolved_minutes(example), 45)
        self.assertEqual(oppgave4.sum_resolved_minutes([]), 0)


class Oppgave5Test(unittest.TestCase):
    def make_activity(self, **overrides):
        data = {'title': 'Run', 'category': 'sport', 'date': '28.09.2026', 'estimated_minutes': 40, 'status': 'planned'}
        data.update(overrides)
        return Activity.from_dict(data)

    def test_dict_roundtrip(self):
        activity = self.make_activity()
        self.assertEqual(activity.date, date(2026, 9, 28))
        self.assertEqual(Activity.from_dict(activity.to_dict()).to_dict(), activity.to_dict())

    def test_from_dict_invalid(self):
        for overrides in [
            {'title': ' '}, {'estimated_minutes': 0}, {'estimated_minutes': '40'},
            {'status': 'done'}, {'date': '31.02.2026'},
        ]:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.make_activity(**overrides)
        with self.assertRaises(KeyError):
            Activity.from_dict({'title': 'x'})

    def test_mark_completed(self):
        activity = self.make_activity()
        self.assertTrue(activity.mark_completed())
        self.assertFalse(activity.mark_completed())
        self.assertEqual(activity.status, 'completed')

    def test_register_with_validation(self):
        activities = []
        _, output = run_with_input(
            oppgave5.register_activity,
            ['', 'Swim', 'sport', '31.02.2026', '30.09.2026', '0', '45', 'done', 'planned'],
            activities,
        )
        self.assertEqual(len(activities), 1)
        self.assertEqual(str(activities[0]), 'Swim | sport | 30.09.2026 | 45 min | planned')
        self.assertEqual(output.count('Error'), 4)

    def test_search_filter_sort(self):
        activities = [
            self.make_activity(title='Morning run', estimated_minutes=40, date='28.09.2026'),
            self.make_activity(title='Read docs', category='study', estimated_minutes=60, date='25.09.2026', status='completed'),
        ]
        _, output = run_with_input(oppgave5.search_activities, ['STUDY'], activities)
        self.assertIn('Read docs', output)
        self.assertNotIn('Morning run', output)
        _, output = run_with_input(oppgave5.filter_by_status, ['completed'], activities)
        self.assertEqual(output.count('\n'), 1)
        _, output = run_with_input(oppgave5.sort_activities, ['date'], activities)
        self.assertTrue(output.startswith('1. Read docs'))
        _, output = run_with_input(oppgave5.sort_activities, ['duration'], activities)
        self.assertTrue(output.startswith('1. Read docs'))
        self.assertEqual(activities[0].title, 'Morning run')

    def test_complete_activity(self):
        activities = [self.make_activity(), self.make_activity(title='Swim')]
        _, output = run_with_input(oppgave5.complete_activity, ['3', '2'], activities)
        self.assertEqual(activities[1].status, 'completed')
        self.assertIn('Error', output)
        _, output = run_with_input(oppgave5.complete_activity, [], [])
        self.assertIn('No planned activities', output)

    def test_statistics(self):
        activities = [self.make_activity(), self.make_activity(estimated_minutes=20, status='completed')]
        _, output = run_with_input(oppgave5.show_statistics, [], activities)
        self.assertIn('Activities: 2', output)
        self.assertIn('Total estimated time: 60 min', output)
        self.assertIn('Completed: 1', output)

    def test_save_and_load(self):
        activities = [self.make_activity(), self.make_activity(title='Swim', status='completed')]
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'activities.json')
            run_with_input(oppgave5.save_activities, [], activities, path)
            loaded, output = run_with_input(oppgave5.load_activities, [], path)
            self.assertIn('Loaded 2 activities', output)
            self.assertEqual([a.to_dict() for a in loaded], [a.to_dict() for a in activities])

    def test_load_missing_file(self):
        loaded, output = run_with_input(oppgave5.load_activities, [], 'no-such-file.json')
        self.assertEqual(loaded, [])
        self.assertIn('starting with an empty list', output)

    def test_load_skips_corrupt_entries(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'activities.json')
            with open(path, 'w', encoding='utf-8') as file:
                json.dump([
                    {'title': 'Ok', 'category': 'a', 'date': '01.10.2026', 'estimated_minutes': 10, 'status': 'planned'},
                    {'title': 'Bad', 'category': 'a', 'date': '01.10.2026', 'estimated_minutes': -5, 'status': 'planned'},
                    {'title': 'Missing'},
                ], file)
            loaded, output = run_with_input(oppgave5.load_activities, [], path)
        self.assertEqual([a.title for a in loaded], ['Ok'])
        self.assertIn('Entry 2: skipped', output)
        self.assertIn('Entry 3: skipped', output)

    def test_load_invalid_json_and_wrong_root(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'activities.json')
            with open(path, 'w', encoding='utf-8') as file:
                file.write('{not json')
            loaded, output = run_with_input(oppgave5.load_activities, [], path)
            self.assertEqual(loaded, [])
            self.assertIn('could not read', output)
            with open(path, 'w', encoding='utf-8') as file:
                file.write('{}')
            loaded, output = run_with_input(oppgave5.load_activities, [], path)
            self.assertEqual(loaded, [])
            self.assertIn('does not contain a list', output)

    def test_merge_replace_and_add(self):
        activities = [self.make_activity()]
        new_items = [self.make_activity(title='New')]
        run_with_input(oppgave5.merge_activities, ['replace'], activities, new_items)
        self.assertEqual([a.title for a in activities], ['New'])
        run_with_input(oppgave5.merge_activities, ['add'], activities, [self.make_activity(title='More')])
        self.assertEqual([a.title for a in activities], ['New', 'More'])

    def test_clear_requires_confirmation(self):
        activities = [self.make_activity()]
        run_with_input(oppgave5.clear_activities, ['n'], activities)
        self.assertEqual(len(activities), 1)
        run_with_input(oppgave5.clear_activities, ['y'], activities)
        self.assertEqual(activities, [])


if __name__ == '__main__':
    unittest.main()
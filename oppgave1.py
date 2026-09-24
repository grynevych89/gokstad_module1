from helpers import read_integer, read_text, run_menu


# 1.1 Calculate time spent
def calculation_of_time_spent():
    number_of_study_sessions = read_integer('Number of study sessions? ', 1)
    minutes_per_session = read_integer('Minutes per session? ', 1)
    total_time_spent = number_of_study_sessions * minutes_per_session
    hours = total_time_spent // 60
    minutes = total_time_spent % 60
    print(f'Total time spent: {hours} hours, {minutes} minutes')


# 1.2 Analyze text
def text_analysis():
    text = read_text()
    without_spaces = ''.join(text.split())
    print(text)
    print('Length without spaces:', len(without_spaces))
    print('Length with spaces:', len(text))
    print('Without spaces:', without_spaces)
    print('Lowercase:', text.lower())
    print('Reversed:', text[::-1])
    print('Contains "python":', 'python' in text.lower())


# 1.3 Analyze number range
def numeric_range_analysis():
    start_number = read_integer('Enter start number: ')
    end_number = read_integer('Enter end number: ')
    if start_number > end_number:
        start_number, end_number = end_number, start_number

    numbers = range(start_number, end_number + 1)
    evens = [n for n in numbers if n % 2 == 0]
    div_by_three = [n for n in numbers if n % 3 == 0]
    print('Even numbers:', evens)
    print('Divisible by 3:', div_by_three)
    print('Sum:', sum(numbers))


# 1.4 Menu
def main():
    run_menu('MENU', [
        ('Calculate time spent', calculation_of_time_spent),
        ('Analyze text', text_analysis),
        ('Analyze number range', numeric_range_analysis),
    ])


if __name__ == '__main__':
    main()

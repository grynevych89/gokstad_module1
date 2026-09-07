# Helper functions
def read_integer(prompt: str, minimum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Error: please enter a valid integer.')
            continue
        if minimum is None or value >= minimum:
            return value
        print(f'Error: value must be at least {minimum}.')


def read_text(prompt: str = 'Enter text: ') -> str:
    while True:
        text_example = input(prompt)
        if not text_example.strip():
            print('Error: text must not be empty or consist of spaces only!')
            continue
        return text_example


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
    text_example = read_text()
    without_spaces = ''.join(text_example.split())
    print(text_example)
    print('Length without spaces:', len(without_spaces))
    print('Length with spaces:', len(text_example))
    print('Without spaces:', without_spaces)
    print('Lowercase:', text_example.lower())
    print('Reversed:', text_example[::-1])
    print('Contains "python":', 'python' in text_example.lower())


# 1.3 Analyze number range
def numeric_range_analysis():
    start_number = read_integer('Enter start number: ')
    end_number = read_integer('Enter end number: ')
    if start_number > end_number:
        start_number, end_number = end_number, start_number

    numbers = range(start_number, end_number + 1)
    evens = [n for n in numbers if n % 2 == 0]
    div_by_three = [n for n in numbers if n % 3 == 0]
    total_sum = sum(numbers)
    print('Even numbers:', evens)
    print('Divisible by 3:', div_by_three)
    print('Sum:', total_sum)


# 1.4 Menu
def main():
    while True:
        # Отображение меню в терминале
        print('\n=== MENU ===')
        print('1. Calculate time spent')
        print('2. Analyze text')
        print('3. Analyze number range')
        print('4. Exit')
        print('============')

        choice = input('Select an option (1-4): ').strip()

        if choice == '1':
            print('\n--- [Running: 1. Calculate time spent] ---')
            calculation_of_time_spent()
        elif choice == '2':
            print('\n--- [Running: 2. Analyze text] ---')
            text_analysis()  # example: Hello World!@Python
        elif choice == '3':
            print('\n--- [Running: 3. Analyze number range] ---')
            numeric_range_analysis()
        elif choice == '4':
            print('\nProgram exiting. Goodbye!')
            break
        else:
            print('\n[Error]: Invalid choice. Please enter a number between 1 and 4.')


if __name__ == '__main__':
    main()

# 1.1

def read_non_negative(prompt, non_negative_number):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Please enter valid number')
            continue
        if value >= non_negative_number:
            return value
        print('Please enter valid number')


def calculation_of_time_spent():
    non_negative_number = 1
    number_of_study_sessions = read_non_negative('Number of study sessions? ', non_negative_number)
    minutes_per_session = read_non_negative('Minutes per session? ', non_negative_number)

    total_time_spent = number_of_study_sessions * minutes_per_session
    hours = total_time_spent // 60
    minutes = total_time_spent % 60
    print('Total time spent: ' + str(hours) + ' hours, ' + str(minutes) + ' minutes')


# calculation_of_time_spent()


# 1.2

def read_text(prompt='Enter text: ') -> str:
    while True:
        text_example = input(prompt)
        if not text_example.strip():
            print("Error: text must not be empty or consist of spaces only!")
            continue
        return text_example


def text_analysis():
    text_example = read_text()
    print(text_example)
    print(len(text_example.replace(' ', '')))
    print(len(text_example))
    print(text_example.replace(' ', ''))
    print(text_example.lower())
    print(text_example[::-1])
    print('python' in text_example.lower())


# example: Hello World!@Python
# text_analysis()


# 1.3

def is_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: both values must be integers.")


def numeric_range_analysis():
    start_number = is_integer("Enter start number: ")
    end_number = is_integer("Enter end number: ")
    if start_number > end_number:
        start_number, end_number = end_number, start_number

    numbers = range(start_number, end_number + 1)
    evens = [n for n in numbers if n % 2 == 0]
    div_by_three = [n for n in numbers if n % 3 == 0]
    total_sum = sum(numbers)
    print(evens)
    print(div_by_three)
    print(total_sum)


numeric_range_analysis()

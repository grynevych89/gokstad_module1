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

calculation_of_time_spent()

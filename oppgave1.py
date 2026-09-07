# 1.1

def read_non_negative(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Please enter valid number')
            continue
        if value > 0:
            return value
        print('Please enter valid number')

def calculation_of_time_spent():
    number_of_study_sessions = read_non_negative('Number of study sessions? ')
    minutes_per_session = read_non_negative('Minutes per session? ')

    total_time_spent = number_of_study_sessions * minutes_per_session
    hours = total_time_spent // 60
    minutes = total_time_spent % 60
    print('Total time spent: ' + str(hours) + ' hours, ' + str(minutes) + ' minutes')

calculation_of_time_spent()


from datetime import datetime,time,date,timedelta


def valid_str(text):
    valid = False
    while not valid:
        user = input(text).strip()
        if user:
            valid = user
        else:
            print('Cannot be empty.')
    return valid


def valid_float(text):
    valid = False
    while not valid:
        try:
            num = float(input(text))
            if num > 0:
                valid = num
            else:
                print('The number must be greater than 0.')
        except ValueError:
            print('Must be a number.')
    return valid


def valid_date():
    valid = False
    while not valid:
        user_input = input('Select a date  (YYYY-MM-DD): ')
        try:
            parsed_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            if parsed_date >= date.today():
                valid = parsed_date
            else:
                print('Date cannot be in the past.')
        except ValueError:
            print('Invalid format. Please use YYYY-MM-DD.')
    return valid


def valid_time(selected_date):
    valid = False
    while not valid:
        user = input('Select a time (HH:MM): ')
        try:
            user_time = datetime.strptime(user, "%H:%M").time()
            full_datetime = datetime.combine(selected_date, user_time)
            if full_datetime > datetime.now():
                valid = full_datetime
            else:
                print('The selected time has already passed today. Please choose a future time.')
        except ValueError:
            print('Invalid format. Please use HH:MM.')
    return valid

def valid_bike_type():
    valid = False
    while not valid:
        user = valid_str('Enter bike type: (Electric, Mountain, Regular): ').capitalize()
        if user in ['Electric', 'Mountain', 'Regular']:
            valid = user
        else:
            print('Invalid bike type. Please choose from Electric, Mountain, or Regular.')
    return valid



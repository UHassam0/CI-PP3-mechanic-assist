import re
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET_CARS = GSPREAD_CLIENT.open('Car Models')
SHEET = GSPREAD_CLIENT.open('Mechanic-Customers')


def get_name():
    """
    Input function to get customer name
    """
    while True:

        name = input('Customer Name: ')

        if validate_name(name):
            break

    return name


def validate_name(name):
    """
    Validate name input to ensure it is at least 2 letters and not blank
    """
    try:
        str(name)
        if len(name.strip()) < 2:
            print('Input name must be at least 2 letters')
            return False
    except ValueError:
        print('Must input name with regular characters. Check formatting')
        return False
    return True


def get_phone():
    """
    Input function to get customer phone number
    """
    while True:
        phone = input('Customer Phone: ')

        if validate_phone(phone):
            print('number valid')
            break
    return phone


def validate_phone(number):
    """
    Validates phone number according to UK standard landlines and mobiles
    """
    pattern = r"^\+44\d{10}$|^07\d{9}$|^01\d{9}$|^02\d{9}$"

    regex = re.compile(pattern)

    if not regex.match(number):
        print('Number invalid. try again')
        return False

    return True


def get_make():
    """
    Get customer car make
    """
    while True:
        make = input('Car Make: ')

        if validate_make(make):
            print('make accepted')
            break
    return make


def validate_make(make_name):
    """
    Validate customer car make against spreadsheet
    """

    if SHEET_CARS.worksheet('Complete List of Car Brands').find(
        make_name, None, None, False
        ) is None:
        print('Make not accepted please check format and try again')
        return False

    return True


def get_model(make):
    """
    Get customer car model 
    """
    while True:
        model = input('Car Model: ')

        if validate_model(model, make):
            print('model accepted')
            break

    return model


def validate_model(model_name, make):
    """
    Validate car model against worksheet for the make selected
    """
    make_caps = make.capitalize()

    if SHEET_CARS.worksheet(make_caps).find(
        f'{make_caps} {model_name.capitalize()}'
        ) is None:
        print('Model not accepted please check format and try again')
        return False

    return True


def get_age():
    """
    Get car age
    """
    while True:
        age = input('Car Age (in years as a whole number): ')

        if validate_age(age):
            print('Age accepted')
            break
    return age


def validate_age(car_age):
    """
    Validate car age as whole number under 30
    """
    try:
        age = int(car_age)
        if age >= 0 and age <= 30:
            return True
        else:
            print('Car age must be between 1 and 30')
            return False
    except ValueError:
        print('Car age must be whole number as number not letters')
        return False
        
    return True


def get_mileage(car_age):
    """
    get car mileage
    """
    while True:
        mileage = input('Car Mileage: ')

        if validate_mileage(mileage, car_age):
            print('Mileage valid and accepted')
            break

    return mileage


def validate_mileage(mile_number, car_age):
    """
    validate mileage as number and request confirmation if 
    beyond 10% of average for age
    """
    try:
        mileage = int(mile_number)
    except ValueError:
        print('mileage must be a number')
        return False

    average_mileage = int(car_age) * 10000
    if mileage <= average_mileage * 1.1 and mileage >= average_mileage * 0.9:
        return True
    else:
        sure = input('Mileage is outside average range. Are you sure? Y/N ')
        if sure.upper() == 'Y':
            print('you have chosen to input non-average mileage')
            return True
        else:
            print('try again')
            return False


def get_mot():
    """
    Get Next MOT due date
    """
    while True:
        mot_date = input('Next MOT Due Date (DD/MM/YYYY): ')

        if validate_mot(mot_date):
            print('Date Accepted')
            break

    return mot_date


def validate_mot(date):
    """
    Validate MOT date as date within the next year
    """
    try:
        next_mot = datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        print('Date invalid. Try again')
        return False

    today = datetime.now().date()
    next_year = today + timedelta(days=365)

    if next_mot.date() < today or next_mot.date() > next_year:
        print('Date must be within the next year')
        return False

    return True


def survey():
    """
    Gather data for survey and then append to list and google sheet
    """
    print('You have chosen to complete a survey...')
    print(
      'Please fill in the details below. Each will be validated one at a time'
        )
    customer_name = get_name().title()
    customer_phone = get_phone()
    car_make = get_make().capitalize()
    car_model = get_model(car_make)
    car_age = get_age()
    car_mileage = get_mileage(car_age)
    next_mot = get_mot()
    

survey()

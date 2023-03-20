import re
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
        if len(name.strip()) < 3:
            print('Must input name at least 2 letters')
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

    if SHEET_CARS.worksheet('Complete List of Car Brands').find(make_name, None, None, False) is None:
        print('Make not accepted please check format and try again')
        return False

    return True


def survey():
    """
    Gather data for survey and then append to list and google sheet
    """
    print('You have chosen to complete a survey...')
    customer_name = get_name().title()
    customer_phone = get_phone()
    car_make = get_make().capitalize()


survey()

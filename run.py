import re
from tabulate import tabulate
from datetime import datetime, timedelta
import statistics
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

        name = input('Customer Name: \n')

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
        phone = input('Customer Phone: \n')

        if validate_phone(phone):
            print('Number valid')
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
        make = input('Car Make: \n')

        if validate_make(make):
            print('Make accepted')
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
        model = input('Car Model: \n')

        if validate_model(model, make):
            print('Model accepted')
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
        age = input('Car Age (in years as a whole number): \n')

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
    Get car mileage
    """
    while True:
        mileage = input('Car Mileage: \n')

        if validate_mileage(mileage, car_age):
            print('Mileage valid and accepted')
            break

    return mileage


def validate_mileage(mile_number, car_age):
    """
    Validate mileage as number and request confirmation if
    beyond 10% of average for age
    """
    try:
        mileage = int(mile_number)
    except ValueError:
        print('Mileage must be a number')
        return False

    average_mileage = int(car_age) * 10000
    if mileage <= average_mileage * 1.1 and mileage >= average_mileage * 0.9:
        return True
    else:
        sure = input('Mileage is outside average range. Are you sure? Y/N \n')
        if sure.upper() == 'Y':
            print('You have chosen to input non-average mileage')
            return True
        else:
            print('Try again')
            return False


def get_mot():
    """
    Get Next MOT due date
    """
    while True:
        mot_date = input('Next MOT Due Date (DD/MM/YYYY): \n')

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
    print('You have chosen to complete a survey...\n')
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

    print('\nAdding data to database...\n')
    current_values = SHEET.worksheet('Customer-Information').get_all_values()
    latest_id = current_values[-1][0]
    data = [int(latest_id) + 1, customer_name, customer_phone,
            car_make, car_model, car_age, car_mileage, next_mot]
    SHEET.worksheet('Customer-Information').append_row(data)
    print('Data Added\n')


def top_model():
    """
    Calculate most popular car model
    """
    models = SHEET.worksheet('Customer-Information').col_values(5)
    model_popular = statistics.mode(models)

    return model_popular


def average_age():
    """
    Calculate average age of cars in spreadsheet
    """
    age_list = SHEET.worksheet('Customer-Information').col_values(6)
    del age_list[0]
    age_ints = [int(age) for age in age_list]
    average_age = sum(age_ints) / len(age_ints)

    return round(average_age, 1)


def avg_mileage():
    """
    Calculate average mileage of cars in spreadsheet
    """
    mileage_list = SHEET.worksheet('Customer-Information').col_values(7)
    del mileage_list[0]
    mileage_ints = [int(mileage) for mileage in mileage_list]
    avg_mileage = sum(mileage_ints) / len(mileage_ints)

    return round(avg_mileage)


def mots_soon():
    """
    Present list of upcoming MOTs due in next 8 weeks
    """
    print('Getting data for MOTs due in the next 8 weeks...\n')
    today = datetime.now().date()
    eight_weeks = today + timedelta(days=84)

    all_customers = SHEET.worksheet('Customer-Information').get_all_values()

    mots_due = []
    for row in all_customers:
        if row[7] != 'Next MOT due' and row[8] != 'Y':
            date = datetime.strptime(row[7], '%d/%m/%Y').date()
            if today <= date <= eight_weeks:
                mots_due.append(row)
    table_head = SHEET.worksheet('Customer-Information').row_values(1)
    print(tabulate(mots_due, headers=table_head))
    update(mots_due)


def update(mots_booked):
    """
    Get and validate cust ID to update spreadsheet to indicate MOT booked
    """
    while True:
        print()
        cust_id = input('\nYou can now call these customers to book MOTs.\n' +
                        'Enter id of customer booked in.\n' +
                        'Or enter M to return to main menu: \n')

        ids_due = []

        for row in mots_booked:
            ids_due.append(row[0])

        if cust_id in ids_due:
            SHEET.worksheet('Customer-Information').update_cell(
                int(cust_id) + 1, 9, 'Y'
                )
            break
        elif cust_id.upper() == 'M':
            break
        print('That is not one of the IDs above.\n' +
              'Try again or enter M to return to main menu')


def query():
    """
    Combine the various functions to get data and print to terminal
    """
    print('You have chosen to query the stored data\n')
    model = top_model()
    age = average_age()
    mileage = avg_mileage()
    print(f'The most common model amongst our customers is: {model}')
    print(f'The average car age amongst our customers is: {age}')
    print(f'The average car mileage amongst our customers is: {mileage}\n')
    mots_soon()


def main():
    """
    Set the top layer of the program for the user to
    always loop through the various functions
    """
    print('Welcome to Mechanic Assist, where we help you record and query\n' +
          'customer data to get those MOTs booked in\n')
    while True:
        selection = input('Press 1 to record customer info or 2 to query: \n')

        if selection == '1':
            survey()
        elif selection == '2':
            query()
        else:
            print('Sorry input not recognised try again. Must be 1 or 2')


main()

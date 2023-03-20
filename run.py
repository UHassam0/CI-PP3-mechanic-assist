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

get_name()
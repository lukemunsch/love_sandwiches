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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales info from user input
    """
    print("Please enter sales data from the last day of market.")
    print("Data should be in the format of of 6 number, commas with no space between each.")
    print("ex. 33,23,24,45,56,52\n")

    data_str = input("Enter your figures here: ")
    print(f"The data provided is {data_str}")


get_sales_data()


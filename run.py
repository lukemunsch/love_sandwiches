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
    while True:
        print("Please enter sales data from the last day of market.")
        print("Data should be in the format of of 6 number, commas with no space between each.")
        print("ex. 33,23,24,45,56,52\n")

        data_str = input("Enter your figures here: ")

        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is Valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside our try, converts all string values to integers
    raises valueerror if string cannot be converted to in
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid Data: {e}, please try again.")
        return False

    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with list data provided
    """
    print("Updating sales data into worksheet\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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


def update_worksheet(data, worksheet):
    """
    receives a list of integers to be inserted into a worksheet
    updating the relevant worksheet with
    """
    print(f"Updating {worksheet} worksheet\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    compare sales lines of data to work out surplus
    the surplus is defined as the sales figure subtracted from the stock
    -positive outcome means food thrown away
    - negative outcome is food made extra once sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """
    run all programme functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("welcome to Love Sandwiches Data Autmoation!\n")
main()



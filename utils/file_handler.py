# utils/file_handler.py
import pandas as pd
from datetime import datetime
import os

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "expenses.csv")

def init_file():
    # Create folder if missing
    folder = os.path.dirname(FILE_PATH)
    os.makedirs(folder, exist_ok=True)
    # Create CSV with header if missing or empty
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
        df.to_csv(FILE_PATH, index=False)

def add_expense(category, description, amount):
    init_file()
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")
    new_entry = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Category": category.capitalize(),
        "Description": description,
        "Amount": amount
    }])
    df = pd.read_csv(FILE_PATH)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    return True

def view_expenses():
    init_file()
    df = pd.read_csv(FILE_PATH)
    return df

def delete_expense(index):
    init_file()
    df = pd.read_csv(FILE_PATH)
    if index not in df.index:
        raise IndexError("Index out of range.")
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(FILE_PATH, index=False)
    return True
def edit_expense(index, category=None, description=None, amount=None):
    init_file()
    df = pd.read_csv(FILE_PATH)

    if index not in df.index:
        raise IndexError("Invalid index. Please enter a valid row number.")

    if category:
        df.at[index, "Category"] = category.capitalize()
    if description:
        df.at[index, "Description"] = description
    if amount:
        try:
            df.at[index, "Amount"] = float(amount)
        except ValueError:
            raise ValueError("Amount must be a number.")

    df.to_csv(FILE_PATH, index=False)
    return True
def add_expense(category, description, amount, date=None):
    init_file()
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")
    
    if date is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    
    new_entry = pd.DataFrame([{
        "Date": date_str,
        "Category": category.capitalize(),
        "Description": description,
        "Amount": amount
    }])
    df = pd.read_csv(FILE_PATH)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    return True
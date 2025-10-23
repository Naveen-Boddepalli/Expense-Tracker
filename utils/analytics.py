# utils/analytics.py
import pandas as pd
import os

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "expenses.csv")

def total_spent():
    df = pd.read_csv(FILE_PATH)
    if df.empty:
        return 0.0
    return float(df["Amount"].sum())

def category_breakdown():
    df = pd.read_csv(FILE_PATH)
    if df.empty:
        return {}
    grouped = df.groupby("Category")["Amount"].sum().to_dict()
    # convert numpy types to native python floats
    return {k: float(v) for k, v in grouped.items()}

def monthly_summary(year=None, month=None):
    df = pd.read_csv(FILE_PATH)
    if df.empty:
        return pd.DataFrame()
    df["Date"] = pd.to_datetime(df["Date"])
    if year is not None:
        df = df[df["Date"].dt.year == int(year)]
    if month is not None:
        df = df[df["Date"].dt.month == int(month)]
    return df
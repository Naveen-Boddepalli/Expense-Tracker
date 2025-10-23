# utils/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "expenses.csv")

def plot_expenses(show=True, save_path=None):
    df = pd.read_csv(FILE_PATH)
    if df.empty:
        print("No expense data to plot.")
        return None
    category_sum = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Expenses by Category")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    plt.close(fig)
    return True
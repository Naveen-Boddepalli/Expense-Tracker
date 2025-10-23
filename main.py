# main.py
from utils.file_handler import add_expense, view_expenses, delete_expense
from utils.analytics import total_spent, category_breakdown
from utils.visualizer import plot_expenses
import pandas as pd

def menu():
    while True:
        print("\n====== Personal Expense Tracker ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Summary")
        print("4. Plot Expenses (pie chart)")
        print("5. Delete an entry by index")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()
            amount = input("Enter amount: ").strip()
            try:
                add_expense(category, description, amount)
                print("✅ Expense added.")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            df = view_expenses()
            if df.empty:
                print("No expenses found.")
            else:
                print(df.to_string(index=True))

        elif choice == "3":
            total = total_spent()
            breakdown = category_breakdown()
            print(f"\nTotal spent: {total:.2f}")
            print("Category breakdown:")
            for k, v in breakdown.items():
                print(f"  {k}: {v:.2f}")

        elif choice == "4":
            plot_expenses(show=True)

        elif choice == "5":
            df = view_expenses()
            if df.empty:
                print("No expenses to delete.")
                continue
            print(df.to_string(index=True))
            try:
                idx = int(input("Enter index to delete: ").strip())
                delete_expense(idx)
                print("✅ Deleted.")
            except Exception as e:
                print("Error:", e)

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
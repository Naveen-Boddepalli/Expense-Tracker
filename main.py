from utils.file_handler import add_expense, view_expenses, delete_expense, edit_expense
from utils.analytics import total_spent, category_breakdown
from utils.visualizer import plot_expenses
from utils.pdf_report import export_monthly_report
import pandas as pd

def menu():
    while True:
        print("\n====== Personal Expense Tracker ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Summary")
        print("4. Plot Expenses (pie chart)")
        print("5. Delete an entry by index")
        print("6. Edit an entry by index")
        print("7. Export Monthly PDF Report")
        print("8. Exit")
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
            df = view_expenses()
            if df.empty:
                print("No expenses to edit.")
                continue
            print(df.to_string(index=True))
            try:
                idx = int(input("Enter index to edit: ").strip())
                print("\nLeave a field blank to keep it unchanged.")
                new_cat = input("New category: ").strip()
                new_desc = input("New description: ").strip()
                new_amt = input("New amount: ").strip()

                # Replace empty fields with None
                new_cat = new_cat if new_cat else None
                new_desc = new_desc if new_desc else None
                new_amt = new_amt if new_amt else None

                edit_expense(idx, new_cat, new_desc, new_amt)
                print("✅ Expense updated successfully.")
            except Exception as e:
                print("Error:", e)
        elif choice == "7":
            print("\nLeave blank to use current month/year.")
            year = input("Enter year (YYYY): ").strip()
            month = input("Enter month (1-12): ").strip()

            year = int(year) if year else None
            month = int(month) if month else None

            export_monthly_report(year, month)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
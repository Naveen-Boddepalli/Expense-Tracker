import streamlit as st
import pandas as pd
from utils.file_handler import add_expense, view_expenses, delete_expense, edit_expense
from utils.analytics import total_spent, category_breakdown
from utils.visualizer import plot_expenses
from utils.pdf_report import export_monthly_report
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("💰 Personal Expense Tracker")

# Sidebar menu
menu = ["Add Expense", "View Expenses", "Edit Expense", "Delete Expense", "Summary", "Plot Expenses", "Export PDF"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- ADD EXPENSE ----------------
if choice == "Add Expense":
    st.subheader("Add New Expense")
    categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
    with st.form("add_expense_form"):
        category = st.selectbox("Category", categories)
        description = st.text_input("Description")
        amount = st.text_input("Amount")
        date = st.date_input("Date")  # date picker
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            try:
                add_expense(category, description, amount, date)
                st.success("✅ Expense added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- VIEW EXPENSES ----------------
elif choice == "View Expenses":
    st.subheader("All Expenses")
    df = view_expenses()
    if df.empty:
        st.info("No expenses recorded yet.")
    else:
        st.dataframe(df)

# ---------------- EDIT EXPENSE ----------------
elif choice == "Edit Expense":
    st.subheader("Edit an Expense")
    df = view_expenses()
    if df.empty:
        st.info("No expenses to edit.")
    else:
        st.dataframe(df)
        index = st.number_input("Enter index to edit", min_value=0, max_value=len(df)-1, step=1)
        new_category = st.text_input("New Category (leave blank to keep)")
        new_desc = st.text_input("New Description (leave blank to keep)")
        new_amount = st.text_input("New Amount (leave blank to keep)")
        if st.button("Update Expense"):
            try:
                edit_expense(index,
                             new_category if new_category else None,
                             new_desc if new_desc else None,
                             new_amount if new_amount else None)
                st.success("✅ Expense updated successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- DELETE EXPENSE ----------------
elif choice == "Delete Expense":
    st.subheader("Delete an Expense")
    df = view_expenses()
    if df.empty:
        st.info("No expenses to delete.")
    else:
        st.dataframe(df)
        index = st.number_input("Enter index to delete", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete"):
            try:
                delete_expense(index)
                st.success("✅ Expense deleted!")
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- SUMMARY ----------------
elif choice == "Summary":
    st.subheader("Expense Summary")
    df = view_expenses()
    
    total = total_spent()
    breakdown = category_breakdown()
    st.metric("Total Spent", f"{total:.2f}")
    st.metric("Total Entries", len(df))  
    if breakdown:
        st.bar_chart(breakdown)
    else:
        st.info("No expenses to show in chart.")

# ---------------- PLOT EXPENSES ----------------
elif choice == "Plot Expenses":
    st.subheader("Expenses Pie Chart")
    df = view_expenses()
    if df.empty:
        st.info("No data to plot.")
    else:
        fig, ax = plt.subplots()
        df.groupby("Category")["Amount"].sum().plot.pie(autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)
    colors_list = ["#FF9999","#66B2FF","#99FF99","#FFCC99","#C2C2F0","#FFB266"]
    df.groupby("Category")["Amount"].sum().plot.pie(autopct="%1.1f%%", colors=colors_list, ax=ax)

# ---------------- EXPORT PDF ----------------
elif choice == "Export PDF":
    st.subheader("Export Monthly PDF Report")
    year = st.text_input("Year (leave blank = current)")
    month = st.text_input("Month (1-12, leave blank = current)")
    if st.button("Generate PDF"):
        try:
            year_val = int(year) if year else None
            month_val = int(month) if month else None
            filename = export_monthly_report(year_val, month_val)
            if filename:
                with open(filename, "rb") as f:
                    st.download_button("Download PDF", f, file_name=filename.split("/")[-1])
        except Exception as e:
            st.error(f"Error: {e}")

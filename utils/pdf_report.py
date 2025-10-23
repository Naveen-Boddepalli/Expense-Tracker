from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import pandas as pd
import os
from datetime import datetime
from utils.analytics import monthly_summary

REPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORT_FOLDER, exist_ok=True)

def export_monthly_report(year=None, month=None):
    df = monthly_summary(year, month)
    if df.empty:
        print("No data available for this month.")
        return None

    # Default to current month/year
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    month_name = datetime(year, month, 1).strftime("%B")

    filename = os.path.join(REPORT_FOLDER, f"Expense_Report_{month_name}_{year}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Monthly Expense Report - {month_name} {year}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Total Expenses: {df['Amount'].sum():.2f}")

    # Table Header
    c.setFillColor(colors.gray)
    c.rect(50, height - 120, width - 100, 20, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.drawString(55, height - 115, "Date")
    c.drawString(150, height - 115, "Category")
    c.drawString(300, height - 115, "Description")
    c.drawString(500, height - 115, "Amount")

    c.setFillColor(colors.black)
    y = height - 140
    for _, row in df.iterrows():
        c.drawString(55, y, row["Date"])
        c.drawString(150, y, row["Category"])
        c.drawString(300, y, str(row["Description"]))
        c.drawString(500, y, f"{row['Amount']:.2f}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print(f"✅ Monthly report saved: {filename}")
    return filename
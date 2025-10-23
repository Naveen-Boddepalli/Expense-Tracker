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
    for i, (_, row) in enumerate(df.iterrows()):
        date_str = pd.to_datetime(row["Date"]).strftime("%Y-%m-%d")
        category = str(row["Category"])
        desc = str(row["Description"])
        amount = f"{row['Amount']:.2f}"

        # Wrap long descriptions
        max_chars = 35
        desc_lines = [desc[i:i+max_chars] for i in range(0, len(desc), max_chars)]
        for line in desc_lines:
            c.drawString(55, y, date_str)
            c.drawString(150, y, category)
            c.drawString(300, y, line)
            c.drawString(500, y, amount)
            y -= 20
            if y < 50:
                c.showPage()
                # Repeat table header
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.gray)
                c.rect(50, 800, 500, 20, fill=True, stroke=False)
                c.setFillColor(colors.white)
                c.drawString(55, 805, "Date")
                c.drawString(150, 805, "Category")
                c.drawString(300, 805, "Description")
                c.drawString(500, 805, "Amount")
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 12)
                y = 780

    c.save()
    print(f"✅ Monthly report saved: {filename}")
    return filename
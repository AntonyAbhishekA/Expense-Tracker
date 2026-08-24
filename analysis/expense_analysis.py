"""
Standalone Expense Data Analysis Script
=========================================
Run this separately from the Flask app to generate:
  1. A printed summary report in the terminal
  2. Four PNG chart images saved into analysis/charts/

Usage (from the project root):
    python analysis/expense_analysis.py

Requires the same MySQL database used by app.py (see schema.sql).
"""

import os
import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # render charts to files, no GUI needed
import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "expense_tracker"),
    "port": int(os.environ.get("DB_PORT", 3306)),
}

CHART_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHART_DIR, exist_ok=True)


def load_data() -> pd.DataFrame:
    """Pull the entire expenses table into a pandas DataFrame."""
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        print("No data found in the expenses table. Add some expenses first!")
        sys.exit(0)

    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def print_summary(df: pd.DataFrame):
    """Calculate and print core statistics."""
    total = df["amount"].sum()
    average = df["amount"].mean()
    highest = df["amount"].max()
    lowest = df["amount"].min()
    count = len(df)

    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    avg_by_category = df.groupby("category")["amount"].mean().sort_values(ascending=False)
    by_month = df.groupby("month")["amount"].sum().sort_index()
    top_category = by_category.index[0]

    print("=" * 55)
    print("PERSONAL EXPENSE TRACKER — ANALYSIS REPORT")
    print("=" * 55)
    print(f"Total spending:            ₹{total:,.2f}")
    print(f"Number of transactions:    {count}")
    print(f"Average expense:           ₹{average:,.2f}")
    print(f"Highest expense:           ₹{highest:,.2f}")
    print(f"Lowest expense:            ₹{lowest:,.2f}")
    print(f"Most expensive category:   {top_category}")
    print()
    print("-- Spending by Category --")
    for cat, amt in by_category.items():
        print(f"  {cat:<15} ₹{amt:>10,.2f}")
    print()
    print("-- Average Spending per Category --")
    for cat, amt in avg_by_category.items():
        print(f"  {cat:<15} ₹{amt:>10,.2f}")
    print()
    print("-- Monthly Spending --")
    for month, amt in by_month.items():
        print(f"  {month:<10} ₹{amt:>10,.2f}")
    print("=" * 55)


def chart_spending_by_category(df: pd.DataFrame):
    """
    Visualization 1: Spending by Category (Pie Chart)
    Tells us: which categories dominate our overall budget,
    at a glance, as proportions of the whole.
    """
    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(7, 6))
    plt.pie(by_category.values, labels=by_category.index, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "1_spending_by_category.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def chart_monthly_trend(df: pd.DataFrame):
    """
    Visualization 2: Monthly Spending Trend (Line Chart)
    Tells us: whether spending is rising, falling, or stable
    over time — useful for spotting overspending months.
    """
    by_month = df.groupby("month")["amount"].sum().sort_index()
    plt.figure(figsize=(8, 5))
    plt.plot(by_month.index, by_month.values, marker="o", color="#4f46e5")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spent (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "2_monthly_spending_trend.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def chart_payment_method_distribution(df: pd.DataFrame):
    """
    Visualization 3: Payment Method Distribution (Bar Chart)
    Tells us: which payment methods we rely on most,
    useful for understanding spending habits/cash flow.
    """
    by_method = df.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(7, 5))
    plt.bar(by_method.index, by_method.values, color="#06b6d4")
    plt.title("Payment Method Distribution")
    plt.xlabel("Payment Method")
    plt.ylabel("Total Spent (₹)")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "3_payment_method_distribution.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def chart_top_5_categories(df: pd.DataFrame):
    """
    Visualization 4: Top 5 Expense Categories (Horizontal Bar)
    Tells us: our five biggest spending areas, ranked —
    the first places to look when trying to cut costs.
    """
    top5 = df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
    plt.figure(figsize=(7, 5))
    plt.barh(top5.index[::-1], top5.values[::-1], color="#f59e0b")
    plt.title("Top 5 Expense Categories")
    plt.xlabel("Total Spent (₹)")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "4_top_5_categories.png")
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def main():
    df = load_data()
    print_summary(df)
    print("\nGenerating charts...")
    chart_spending_by_category(df)
    chart_monthly_trend(df)
    chart_payment_method_distribution(df)
    chart_top_5_categories(df)
    print(f"\nAll charts saved to: {CHART_DIR}")


if __name__ == "__main__":
    main()

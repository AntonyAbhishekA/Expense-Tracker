"""
Personal Expense Tracker - Flask Application
==============================================
Connects to a MySQL database (set up via MySQL Workbench using schema.sql)
and provides routes for adding, viewing, editing, deleting, filtering,
and analyzing personal expenses.
"""

import os
from datetime import datetime
from collections import OrderedDict

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load DB credentials from a .env file (see .env.example)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "unix_socket": os.getenv("DB_SOCKET"),
}

CATEGORIES = ["Food", "Transport", "Shopping", "Bills",
              "Entertainment", "Education", "Health", "Other"]

PAYMENT_METHODS = ["Cash", "Card", "UPI", "Bank Transfer", "Other"]


def get_db_connection():
    """Open and return a new MySQL connection using DB_CONFIG."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        raise


# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------
@app.route("/")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Summary stats
    cursor.execute("SELECT COUNT(*) AS count, "
                    "COALESCE(SUM(amount),0) AS total, "
                    "COALESCE(AVG(amount),0) AS avg, "
                    "COALESCE(MAX(amount),0) AS max "
                    "FROM expenses")
    stats = cursor.fetchone()

    # Most expensive category
    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)
    top_category_row = cursor.fetchone()
    top_category = top_category_row["category"] if top_category_row else "N/A"

    # Recent transactions (last 5)
    cursor.execute("""
        SELECT id, title, amount, category, date, payment_method
        FROM expenses
        ORDER BY date DESC, id DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        total=stats["total"],
        count=stats["count"],
        avg=stats["avg"],
        max=stats["max"],
        top_category=top_category,
        recent=recent,
    )


# -------------------------------------------------------------------
# ADD EXPENSE
# -------------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        payment_method = request.form.get("payment_method", "").strip()
        description = request.form.get("description", "").strip() or None

        # --- Basic server-side validation ---
        errors = []
        if not title:
            errors.append("Title is required.")
        if not amount:
            errors.append("Amount is required.")
        else:
            try:
                amount_val = float(amount)
                if amount_val <= 0:
                    errors.append("Amount must be greater than zero.")
            except ValueError:
                errors.append("Amount must be a valid number.")
        if category not in CATEGORIES:
            errors.append("Please choose a valid category.")
        if not date:
            errors.append("Date is required.")
        if payment_method not in PAYMENT_METHODS:
            errors.append("Please choose a valid payment method.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("add_expense.html",
                                    categories=CATEGORIES,
                                    payment_methods=PAYMENT_METHODS,
                                    form_data=request.form)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO expenses (title, amount, category, date, payment_method, description)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (title, amount_val, category, date, payment_method, description),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Expense added successfully!", "success")
        return redirect(url_for("expenses_list"))

    return render_template("add_expense.html",
                            categories=CATEGORIES,
                            payment_methods=PAYMENT_METHODS,
                            form_data={})


# -------------------------------------------------------------------
# VIEW / SEARCH / FILTER EXPENSES
# -------------------------------------------------------------------
@app.route("/expenses")
def expenses_list():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    month = request.args.get("month", "").strip()  # format: YYYY-MM

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE %s"
        params.append(f"%{search}%")

    if category:
        query += " AND category = %s"
        params.append(category)

    if month:
        query += " AND DATE_FORMAT(date, '%%Y-%%m') = %s"
        params.append(month)

    query += " ORDER BY date DESC, id DESC"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "expenses.html",
        expenses=expenses,
        categories=CATEGORIES,
        search=search,
        selected_category=category,
        selected_month=month,
    )


# -------------------------------------------------------------------
# EDIT EXPENSE
# -------------------------------------------------------------------
@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        payment_method = request.form.get("payment_method", "").strip()
        description = request.form.get("description", "").strip() or None

        errors = []
        if not title:
            errors.append("Title is required.")
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                errors.append("Amount must be greater than zero.")
        except ValueError:
            errors.append("Amount must be a valid number.")
        if category not in CATEGORIES:
            errors.append("Please choose a valid category.")
        if not date:
            errors.append("Date is required.")
        if payment_method not in PAYMENT_METHODS:
            errors.append("Please choose a valid payment method.")

        if errors:
            for e in errors:
                flash(e, "error")
            cursor.close()
            conn.close()
            return redirect(url_for("edit_expense", expense_id=expense_id))

        cursor.execute(
            """UPDATE expenses
               SET title=%s, amount=%s, category=%s, date=%s,
                   payment_method=%s, description=%s
               WHERE id=%s""",
            (title, amount_val, category, date, payment_method, description, expense_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Expense updated successfully!", "success")
        return redirect(url_for("expenses_list"))

    # GET: fetch existing record to prefill the form
    cursor.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
    expense = cursor.fetchone()
    cursor.close()
    conn.close()

    if not expense:
        flash("Expense not found.", "error")
        return redirect(url_for("expenses_list"))

    return render_template(
        "edit_expense.html",
        expense=expense,
        categories=CATEGORIES,
        payment_methods=PAYMENT_METHODS,
    )


# -------------------------------------------------------------------
# DELETE EXPENSE
# -------------------------------------------------------------------
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Expense deleted.", "success")
    return redirect(url_for("expenses_list"))


# -------------------------------------------------------------------
# ANALYTICS PAGE (renders charts using Chart.js, fed by /api endpoints)
# -------------------------------------------------------------------
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


# -------------------------------------------------------------------
# JSON API ENDPOINTS - used by JavaScript (Chart.js) on the
# Dashboard and Analytics pages, and computed with a bit of pandas.
# -------------------------------------------------------------------
@app.route("/api/summary")
def api_summary():
    import pandas as pd

    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return jsonify({
            "total": 0, "average": 0, "highest": 0, "lowest": 0,
            "count": 0, "top_category": None, "insights": [
                "Add some expenses to see insights here."
            ]
        })

    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])

    total = round(df["amount"].sum(), 2)
    average = round(df["amount"].mean(), 2)
    highest = round(df["amount"].max(), 2)
    lowest = round(df["amount"].min(), 2)
    count = int(len(df))

    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    top_category = by_category.index[0]
    top_category_pct = round((by_category.iloc[0] / total) * 100, 1)

    # Month-over-month comparison for an auto insight
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month")["amount"].sum().sort_index()

    insights = [
        f"{top_category} is your highest spending category.",
        f"{top_category} accounts for {top_category_pct}% of your total expenses.",
    ]

    if len(monthly) >= 2:
        last_month = monthly.iloc[-1]
        prev_month = monthly.iloc[-2]
        if prev_month > 0:
            change_pct = round(((last_month - prev_month) / prev_month) * 100, 1)
            direction = "increased" if change_pct >= 0 else "decreased"
            insights.append(
                f"Your spending {direction} by {abs(change_pct)}% compared with the previous month."
            )

    # Most common payment method
    if "payment_method" in df.columns and not df["payment_method"].isna().all():
        top_payment = df["payment_method"].value_counts().idxmax()
        insights.append(f"You most often pay using {top_payment}.")

    return jsonify({
        "total": total,
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "count": count,
        "top_category": top_category,
        "insights": insights,
    })


@app.route("/api/category-data")
def api_category_data():
    import pandas as pd
    conn = get_db_connection()
    df = pd.read_sql("SELECT category, amount FROM expenses", conn)
    conn.close()

    if df.empty:
        return jsonify({"labels": [], "values": []})

    df["amount"] = df["amount"].astype(float)
    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return jsonify({"labels": grouped.index.tolist(),
                     "values": [round(v, 2) for v in grouped.values.tolist()]})


@app.route("/api/monthly-data")
def api_monthly_data():
    import pandas as pd
    conn = get_db_connection()
    df = pd.read_sql("SELECT date, amount FROM expenses", conn)
    conn.close()

    if df.empty:
        return jsonify({"labels": [], "values": []})

    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    grouped = df.groupby("month")["amount"].sum().sort_index()
    return jsonify({"labels": grouped.index.tolist(),
                     "values": [round(v, 2) for v in grouped.values.tolist()]})


@app.route("/api/payment-method-data")
def api_payment_method_data():
    import pandas as pd
    conn = get_db_connection()
    df = pd.read_sql("SELECT payment_method, amount FROM expenses", conn)
    conn.close()

    if df.empty:
        return jsonify({"labels": [], "values": []})

    df["amount"] = df["amount"].astype(float)
    grouped = df.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
    return jsonify({"labels": grouped.index.tolist(),
                     "values": [round(v, 2) for v in grouped.values.tolist()]})


@app.route("/api/top-categories")
def api_top_categories():
    import pandas as pd
    conn = get_db_connection()
    df = pd.read_sql("SELECT category, amount FROM expenses", conn)
    conn.close()

    if df.empty:
        return jsonify({"labels": [], "values": []})

    df["amount"] = df["amount"].astype(float)
    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
    return jsonify({"labels": grouped.index.tolist(),
                     "values": [round(v, 2) for v in grouped.values.tolist()]})


if __name__ == "__main__":
    app.run(debug=True)

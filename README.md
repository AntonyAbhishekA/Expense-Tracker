# 💰 Personal Expense Tracker

A full-stack web application to record, manage, and analyze personal expenses.
Built with **Python, Flask, MySQL, HTML/CSS/JavaScript, and Pandas**.

## Features

- ✅ Add, view, edit, and delete expenses
- ✅ Categorize expenses (Food, Transport, Shopping, Bills, Entertainment, Education, Health, Other)
- ✅ Search and filter by title, category, and month
- ✅ Dashboard with total spending, average, highest expense, and top category
- ✅ Interactive charts (Chart.js): category breakdown, monthly trend, payment methods, top 5 categories
- ✅ Auto-generated insights calculated live from your data using Pandas
- ✅ Standalone Pandas + Matplotlib analysis script that exports PNG charts
- ✅ Fully responsive design (desktop + mobile)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| Backend | Python, Flask |
| Database | MySQL (via MySQL Workbench) |
| Data Analysis | Pandas, Matplotlib |

## Project Structure

```
expense-tracker/
├── app.py                     # Flask application (routes, DB logic, API endpoints)
├── schema.sql                 # Run this in MySQL Workbench to set up the database
├── requirements.txt           # Python dependencies
├── .env.example                # Template for your DB credentials
├── templates/
│   ├── base.html
│   ├── index.html              # Dashboard
│   ├── add_expense.html
│   ├── edit_expense.html
│   ├── expenses.html           # Expense history + filters
│   └── analytics.html
├── static/
│   ├── css/style.css
│   └── js/
│       ├── script.js           # Nav toggle, delete confirm
│       ├── dashboard.js        # Dashboard charts
│       └── analytics.js        # Analytics page charts
├── analysis/
│   └── expense_analysis.py     # Standalone pandas/matplotlib report + charts
└── README.md
```

## Setup Instructions

### 1. Set up the database in MySQL Workbench

1. Open MySQL Workbench and connect to your local MySQL server.
2. Open `schema.sql` (File → Open SQL Script) and run the entire script
   (⚡ lightning-bolt icon, or `Ctrl+Shift+Enter`).
3. This creates the `expense_tracker` database, the `expenses` table, and
   loads 20 sample rows so your dashboard isn't empty on first run.

### 2. Configure your credentials

```bash
cp .env.example .env
```

Open `.env` and fill in your real MySQL Workbench username/password:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=expense_tracker
DB_PORT=3306
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

### 5. (Optional) Run the standalone analysis script

Generates a text report + 4 PNG charts in `analysis/charts/`:

```bash
python analysis/expense_analysis.py
```

## Database Concepts (Beginner Notes)

- **Database**: an organized collection of data — our filing cabinet, named `expense_tracker`.
- **Table**: like one spreadsheet inside that cabinet — our `expenses` table, with columns (fields) and rows (records).
- **Primary Key**: a column that uniquely identifies each row. Our `id` column is `AUTO_INCREMENT PRIMARY KEY`, so MySQL assigns 1, 2, 3... automatically and guarantees no duplicates.
- **INSERT**: adds a new row — used when you submit the "Add Expense" form.
  ```sql
  INSERT INTO expenses (title, amount, category, date, payment_method, description)
  VALUES ('Groceries', 45.50, 'Food', '2026-06-03', 'Card', 'Weekly shop');
  ```
- **SELECT**: reads rows — used to populate the dashboard and expense list.
  ```sql
  SELECT * FROM expenses ORDER BY date DESC;
  ```
- **UPDATE**: modifies an existing row — used by the "Edit Expense" page.
  ```sql
  UPDATE expenses SET title='Groceries', amount=50.00 WHERE id=3;
  ```
- **DELETE**: removes a row — used by the delete button.
  ```sql
  DELETE FROM expenses WHERE id=3;
  ```
- **WHERE**: filters which rows a query affects. Without it, `UPDATE`/`DELETE` would apply to *every* row — always double-check it's there!

## Visualizations Explained

1. **Spending by Category (Pie/Doughnut)** — shows the proportion of your total spend that goes to each category, making it easy to spot where most of your money goes.
2. **Monthly Spending Trend (Line)** — tracks total spending over time, revealing whether your spending is rising, falling, or stable month to month.
3. **Payment Method Distribution (Bar)** — shows which payment methods (Cash, Card, UPI, etc.) you rely on most.
4. **Top 5 Expense Categories (Horizontal Bar)** — ranks your five biggest spending categories, the natural first place to look when trying to cut costs.

## Notes

- The sample data in `schema.sql` uses dates in **June–July 2026** — feel free to delete it and add your own real expenses.
- All charts are generated live from real database data (via Pandas) — nothing is hardcoded.

-- ============================================
-- Personal Expense Tracker - Database Schema
-- Run this entire file in MySQL Workbench
-- (Query > Run SQL Script, or paste and execute)
-- ============================================

-- Create the database (container for our tables)
CREATE DATABASE IF NOT EXISTS expense_tracker;

-- Tell MySQL to use this database for the statements below
USE expense_tracker;

-- Create the expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Optional: sample data so the dashboard looks
-- populated the first time you run the app.
-- Feel free to delete these rows later from the
-- Expense History page.
-- ============================================
INSERT INTO expenses (title, amount, category, date, payment_method, description) VALUES
('Grocery shopping', 45.50, 'Food', '2026-06-03', 'Card', 'Weekly groceries'),
('Uber to airport', 22.00, 'Transport', '2026-06-05', 'UPI', NULL),
('Netflix subscription', 15.99, 'Entertainment', '2026-06-06', 'Card', 'Monthly subscription'),
('Electricity bill', 60.00, 'Bills', '2026-06-08', 'Bank Transfer', NULL),
('New headphones', 89.99, 'Shopping', '2026-06-10', 'Card', 'Wireless headphones'),
('Doctor visit', 120.00, 'Health', '2026-06-12', 'Cash', 'Routine checkup'),
('Online course', 49.99, 'Education', '2026-06-14', 'Card', 'Python course'),
('Coffee with friend', 8.50, 'Food', '2026-06-15', 'Cash', NULL),
('Movie tickets', 24.00, 'Entertainment', '2026-06-17', 'UPI', NULL),
('Gas fill-up', 40.00, 'Transport', '2026-06-19', 'Card', NULL),
('Restaurant dinner', 55.00, 'Food', '2026-07-02', 'Card', 'Birthday dinner'),
('Internet bill', 35.00, 'Bills', '2026-07-04', 'Bank Transfer', NULL),
('Gym membership', 30.00, 'Health', '2026-07-05', 'Card', 'Monthly fee'),
('Bus pass', 20.00, 'Transport', '2026-07-08', 'Cash', 'Monthly pass'),
('Shoes', 65.00, 'Shopping', '2026-07-10', 'Card', NULL),
('Book purchase', 18.50, 'Education', '2026-07-12', 'UPI', NULL),
('Concert ticket', 75.00, 'Entertainment', '2026-07-15', 'Card', NULL),
('Phone bill', 40.00, 'Bills', '2026-07-18', 'Bank Transfer', NULL),
('Lunch', 12.00, 'Food', '2026-07-20', 'Cash', NULL),
('Pharmacy', 22.30, 'Health', '2026-07-22', 'Card', 'Medicines');

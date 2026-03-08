# Invoice Reconciliation & Dunning Workflow Demo

A lightweight workflow automation demo built with **Flask, Bootstrap, and SQLite**.  
This project simulates how a finance or leasing operations team might handle **invoice reconciliation, exception reporting, overdue invoices, dunning reminders, and audit logging**.

The goal of this demo is to showcase **systems thinking, workflow design, business-rule handling, exception management, and automation-oriented problem solving** in a simple MVP format.

---

## Project Overview

In many operations-heavy businesses, teams need reliable workflows for:

- matching incoming payments to invoices
- identifying partial, unmatched, or duplicate payments
- flagging overdue invoices
- triggering reminder actions
- keeping an audit trail of system activity

This demo simulates those workflows in a simple internal dashboard.

---

## Features

- **Dashboard overview**
  - total invoices
  - total payments
  - open exceptions
  - overdue invoices

- **Invoice list**
  - view invoice number, customer, amount, due date, and status

- **Payment list**
  - view payment references, linked invoices, amounts, dates, and reconciliation status

- **Reconciliation workflow**
  - matched payments
  - partial payments
  - unmatched payments
  - duplicate payment references
  - overdue invoice detection

- **Exception queue**
  - collect and display workflow exceptions for manual review

- **Dunning reminder simulation**
  - simulate reminder actions for overdue invoices

- **Audit logs**
  - record reconciliation runs, reminders, and exception events

---

## Demo Workflow

### 1. Seed sample data
The project loads sample invoices and payments with a mix of normal and edge-case scenarios.

### 2. Run reconciliation
When the user clicks **Run Reconciliation**, the app checks payment and invoice records and applies workflow rules.

### 3. Detect exceptions
The system flags issues such as:

- duplicate payment references
- missing invoice references
- invoice not found
- partial payments
- overpayments
- overdue unpaid invoices

### 4. Send reminders
The user can simulate sending reminders for overdue invoices.

### 5. Review audit trail
All major actions are written to the audit log.

---

## Example Business Rules

This MVP includes rule-based workflow handling such as:

- If payment amount equals invoice amount → mark as **Matched / Paid**
- If payment amount is less than invoice amount → mark as **Partial**
- If payment reference is duplicated → raise **Duplicate exception**
- If invoice number is missing or invalid → raise **Unmatched exception**
- If an unpaid invoice is past due → mark as **Overdue**
- If reminders are triggered → log the action in **Audit Logs**

---

## Tech Stack

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**
- **Bootstrap 5**
- **HTML / Jinja Templates**
- **CSS**

---

## Project Structure

```text
invoice-automation-demo/
├── app.py
├── models.py
├── seed_data.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── invoices.html
│   ├── payments.html
│   ├── exceptions.html
│   └── logs.html
└── static/
    └── style.css
```

## How to Run
1. Clone the repository
```Bash
git clone https://github.com/your-username/invoice-reconciliation-workflow-demo.git
cd invoice-reconciliation-workflow-demo
```
2. Create a virtual environment
Windows
```Bash
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies
```Bash
pip install -r requirements.txt
```
4. Seed demo data
```Bash
python seed_data.py
```
5. Run the application
```Bash
python app.py
```
6. Open in browser
http://127.0.0.1:5000

## Sample Scenarios Included

The demo seed data includes examples of:

### a fully matched payment

### a partial payment

### a payment linked to a non-existent invoice

### a payment with no invoice reference

### a duplicate payment reference

### overdue unpaid invoices

This helps demonstrate both the happy path and exception handling workflows.

## Why I Built This

This project was built to demonstrate a workflow automation mindset for roles involving:

### systems and process design

### finance / operations automation

### reconciliation workflows

### exception management

### low-code / workflow-oriented problem solving

Although this MVP is implemented in Flask rather than a low-code platform, it reflects the same core thinking required in automation roles:
map the workflow, define rules, handle edge cases, test outcomes, and make operations more reliable.

## Possible Future Improvements

### search and filter for invoices/payments

### manual exception resolution actions

### CSV export

### email reminder integration

### role-based user access

### external finance system integration

### visual workflow diagram

### automated scheduler for reconciliation runs

## Screenshots

You can add screenshots here after running the app, for example:

### Dashboard

### Invoices page

### Payments page

### Exception Queue

### Audit Logs

## Author

Edna Zhang

## License

This project is for portfolio and demonstration purposes.

import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"expenses": [], "budgets": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_expense(data):
    date = input("Date (YYYY-MM-DD, default today): ") or datetime.today().strftime('%Y-%m-%d')
    category = input("Category (e.g., Food, Transport, Rent): ")
    amount = float(input("Amount: "))
    note = input("Note (optional): ")

    data["expenses"].append({
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    })
    save_data(data)

    # Budget check
    month = date[:7]
    monthly_total = sum(e["amount"] for e in data["expenses"] if e["category"] == category and e["date"].startswith(month))
    budget = data["budgets"].get(category)
    if budget and monthly_total > budget:
        print(f"⚠️ ALERT: Budget exceeded for {category} this month! (Spent: {monthly_total}, Budget: {budget})")

    print("Expense logged!\n")

def set_budget(data):
    category = input("Set budget for which category? ")
    amount = float(input(f"Enter budget amount for {category}: "))
    data["budgets"][category] = amount
    save_data(data)
    print(f"Budget set for {category}: {amount}\n")

def show_summary(data, days=30):
    since_date = datetime.today() - timedelta(days=days)
    summary = {}

    for expense in data["expenses"]:
        exp_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        if exp_date >= since_date:
            category = expense["category"]
            summary[category] = summary.get(category, 0) + expense["amount"]

    print(f"\n--- Summary (last {days} days) ---")
    for cat, total in summary.items():
        print(f"{cat}: ₹{total:.2f}")
    print()

def export_csv(data):
    if not data["expenses"]:
        print("No data to export.")
        return
    df = pd.DataFrame(data["expenses"])
    filename = "expenses_export.csv"
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}\n")

def plot_expenses(data, days=30):
    since_date = datetime.today() - timedelta(days=days)
    summary = {}

    for expense in data["expenses"]:
        exp_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        if exp_date >= since_date:
            summary[expense["category"]] = summary.get(expense["category"], 0) + expense["amount"]

    if not summary:
        print("No expenses to plot.")
        return

    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title(f"Expenses Breakdown (Last {days} Days)")
    plt.axis('equal')
    plt.show()

def menu():
    data = load_data()
    options = """
Expense Tracker Menu
1. Log Expense
2. View Weekly Summary
3. View Monthly Summary
4. View Budget Status
5. Set Budget
6. Plot Expense Pie Chart
7. Export to CSV
8. Exit
"""
    while True:
        print(options)
        choice = input("Enter choice: ")

        if choice == '1':
            log_expense(data)
        elif choice == '2':
            show_summary(data, days=7)
        elif choice == '3':
            show_summary(data, days=30)
        elif choice == '4':
            print("\n--- Current Budgets ---")
            for k, v in data['budgets'].items():
                print(f"{k}: ₹{v}")
            print()
        elif choice == '5':
            set_budget(data)
        elif choice == '6':
            plot_expenses(data)
        elif choice == '7':
            export_csv(data)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    menu()

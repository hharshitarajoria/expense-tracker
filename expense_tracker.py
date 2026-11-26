"""Expense Tracker - a small command-line app for recording daily expenses."""

import argparse
import json
import os
from datetime import date, datetime

DATA_FILE = "expenses.json"


def load_expenses(path=DATA_FILE):
    """Read expenses from the JSON file, or return an empty list."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def validate_amount(value):
    """Return the amount as a float, or raise ValueError if it is invalid."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{value}' is not a valid amount.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_date(value):
    """Accept YYYY-MM-DD; default to today."""
    if not value:
        return date.today().isoformat()
    return datetime.strptime(value, "%Y-%m-%d").date().isoformat()


def add_expense(expenses, amount, category, expense_date=None, note=""):
    expense = {
        "amount": validate_amount(amount),
        "category": category.strip().lower(),
        "date": validate_date(expense_date),
        "note": note,
    }
    expenses.append(expense)
    return expense


def format_table(expenses):
    if not expenses:
        return "No expenses recorded yet."
    lines = [f"{'#':<4}{'Date':<12}{'Category':<14}{'Amount':>10}  Note", "-" * 52]
    for i, e in enumerate(expenses, start=1):
        lines.append(f"{i:<4}{e['date']:<12}{e['category']:<14}{e['amount']:>10.2f}  {e['note']}")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(description="Track your daily expenses.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an expense")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    add.add_argument("--note", default="")

    sub.add_parser("list", help="List all expenses")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = load_expenses()

    if args.command == "add":
        try:
            e = add_expense(expenses, args.amount, args.category, args.date, args.note)
        except ValueError as err:
            print(f"Error: {err}")
            return 1
        save_expenses(expenses)
        print(f"Added {e['amount']:.2f} to '{e['category']}' on {e['date']}.")
    elif args.command == "list":
        print(format_table(expenses))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

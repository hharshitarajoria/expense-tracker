"""Expense Tracker - a small command-line app for recording daily expenses."""

import argparse
import json
import os
from datetime import date, datetime

DATA_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

# Shares of the monthly budget at which the user is alerted.
# Merge resolution: keep both ideas as two alert levels.
WARNING_THRESHOLD = 0.75   # from feature/early-warning
CRITICAL_THRESHOLD = 0.90  # from feature/critical-alert


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


def filter_by_month(expenses, month=None):
    """Keep only expenses in the given month (YYYY-MM); all if month is None."""
    if not month:
        return list(expenses)
    return [e for e in expenses if e["date"].startswith(month)]


def category_totals(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = round(totals.get(e["category"], 0) + e["amount"], 2)
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))


def format_summary(expenses, month=None):
    selected = filter_by_month(expenses, month)
    title = f"Summary for {month}" if month else "Summary (all time)"
    lines = [title, "-" * 30]
    for category, total in category_totals(selected).items():
        lines.append(f"{category:<16}{total:>12.2f}")
    lines.append("-" * 30)
    lines.append(f"{'TOTAL':<16}{sum(e['amount'] for e in selected):>12.2f}")
    return "\n".join(lines)


def load_budget(path=BUDGET_FILE):
    if not os.path.exists(path):
        return 0.0
    with open(path, "r", encoding="utf-8") as f:
        return float(json.load(f).get("monthly_budget", 0))


def save_budget(amount, path=BUDGET_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"monthly_budget": validate_amount(amount)}, f, indent=2)


def budget_alert(spent, budget):
    """Return an alert message when spending nears or passes the budget."""
    if budget <= 0:
        return None
    ratio = spent / budget
    if ratio >= 1:
        return f"OVER BUDGET: spent {spent:.2f} of {budget:.2f} ({ratio:.0%})."
    if ratio >= CRITICAL_THRESHOLD:
        return f"CRITICAL: you have used {ratio:.0%} of your budget. Only {budget - spent:.2f} left."
    if ratio >= WARNING_THRESHOLD:
        return f"WARNING: you have used {ratio:.0%} of your budget. Consider slowing down."
    return None


def budget_report(expenses, budget, month):
    spent = sum(e["amount"] for e in filter_by_month(expenses, month))
    lines = [
        f"Budget for {month}: {budget:.2f}",
        f"Spent: {spent:.2f}   Remaining: {budget - spent:.2f}",
    ]
    alert = budget_alert(spent, budget)
    if alert:
        lines.append(alert)
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

    summary = sub.add_parser("summary", help="Show totals by category")
    summary.add_argument("--month", default=None, help="YYYY-MM (default: all time)")

    budget = sub.add_parser("budget", help="Set or check the monthly budget")
    budget.add_argument("--set", dest="amount", default=None, help="New monthly budget")
    budget.add_argument("--month", default=date.today().strftime("%Y-%m"), help="YYYY-MM")
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
    elif args.command == "summary":
        print(format_summary(expenses, args.month))
    elif args.command == "budget":
        if args.amount is not None:
            try:
                save_budget(args.amount)
            except ValueError as err:
                print(f"Error: {err}")
                return 1
            print(f"Monthly budget set to {load_budget():.2f}.")
        else:
            print(budget_report(expenses, load_budget(), args.month))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Expense Tracker (CLI)

A small command-line expense tracker written in Python. It was built to practise
Git and GitHub workflows: branching, committing, merging and resolving a merge conflict.

## Requirements
- Python 3.8 or newer (no third-party packages)

## Usage
```bash
python expense_tracker.py add 250 food --date 2026-11-20 --note "Lunch"
python expense_tracker.py list
python expense_tracker.py summary
python expense_tracker.py summary --month 2026-11
```

### Monthly budget and alerts
```bash
python expense_tracker.py budget --set 1800
python expense_tracker.py budget --month 2026-11
```

| Spending vs. budget | Message |
|---|---|
| 75% or more | `WARNING` |
| 90% or more | `CRITICAL` |
| 100% or more | `OVER BUDGET` |

Expenses are stored in `expenses.json` and the budget in `budget.json`, both in the current folder.

## Git workflow used
Each feature was built on its own branch and merged into `main`:
`feature/add-list`, `feature/summary`, `feature/budget-alert`.

A merge conflict was created on purpose: `feature/early-warning` (alert at 75%) and
`feature/critical-alert` (alert at 90%) both changed the same `ALERT_THRESHOLD` line.
It was resolved by keeping both as two alert levels. See [REFLECTION.md](REFLECTION.md).

## Running the tests
```bash
python -m unittest -v
```

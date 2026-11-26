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

Expenses are stored in `expenses.json` in the current folder.

## Running the tests
```bash
python -m unittest -v
```

import unittest

import expense_tracker as et


class ExpenseTrackerTests(unittest.TestCase):
    def test_add_valid_expense(self):
        expenses = []
        e = et.add_expense(expenses, "250", "Food ", "2026-11-20", "Lunch")
        self.assertEqual(e["amount"], 250.0)
        self.assertEqual(e["category"], "food")
        self.assertEqual(len(expenses), 1)

    def test_rejects_invalid_amounts(self):
        for bad in ("abc", "0", "-5"):
            with self.assertRaises(ValueError):
                et.add_expense([], bad, "food")

    def test_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            et.add_expense([], "10", "food", "20-11-2026")

    def test_category_totals_and_month_filter(self):
        expenses = []
        et.add_expense(expenses, "100", "food", "2026-11-01")
        et.add_expense(expenses, "50", "food", "2026-11-02")
        et.add_expense(expenses, "70", "travel", "2026-10-30")
        november = et.filter_by_month(expenses, "2026-11")
        self.assertEqual(et.category_totals(november), {"food": 150.0})
        self.assertEqual(et.category_totals(expenses), {"food": 150.0, "travel": 70.0})

    def test_no_alert_below_threshold(self):
        self.assertIsNone(et.budget_alert(500, 1000))

    def test_warning_level_at_75_percent(self):
        self.assertIn("WARNING", et.budget_alert(780, 1000))

    def test_critical_level_at_90_percent(self):
        self.assertIn("CRITICAL", et.budget_alert(920, 1000))

    def test_over_budget_alert(self):
        self.assertIn("OVER BUDGET", et.budget_alert(1200, 1000))

    def test_no_alert_without_budget(self):
        self.assertIsNone(et.budget_alert(500, 0))


if __name__ == "__main__":
    unittest.main()

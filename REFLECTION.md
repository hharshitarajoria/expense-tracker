# Reflection: Git and GitHub Project with an Intentional Merge Conflict

**Repository:** https://github.com/hharshitarajoria/expense-tracker

## 1. Project and workflow
I built a small command-line **Expense Tracker** in Python. It adds and lists expenses, shows
totals by category and month, and warns when spending nears a monthly budget. Nine unit tests
check the main behaviour.

After `git init` and a first commit (README and `.gitignore`), each feature was built on its
own branch, committed with a clear message and merged into `main` with `git merge --no-ff`:
`feature/add-list`, `feature/summary` and `feature/budget-alert`. The repository was then
published with `git remote add` and `git push`. Commands used: `git init`, `status`, `add`,
`commit`, `checkout -b`, `diff`, `merge`, `log --graph`, `remote`, `push`.

## 2. Creating the merge conflict
From the same commit on `main` I created two branches that changed the same lines differently:

| Branch | `ALERT_THRESHOLD` | Alert message |
|---|---|---|
| `feature/early-warning` | 0.80 → 0.75 | "WARNING … Consider slowing down." |
| `feature/critical-alert` | 0.80 → 0.90 | "CRITICAL … Only X left." |

The first merge succeeded. Merging the second gave
`CONFLICT (content): Merge conflict in expense_tracker.py`.

**Why:** Git merges line by line against the common ancestor. Both branches changed the same
two lines from the same original text, so Git could not tell which version was right and
stopped for a human decision. `git status` showed the file as "both modified" and the file held
`<<<<<<<`, `=======` and `>>>>>>>` markers around each disagreement.

## 3. Resolution
Choosing one side would have discarded the other developer's idea, and the two branches really
wanted different things: an early nudge and an urgent warning. I kept both by replacing the
single threshold with two levels:

```python
WARNING_THRESHOLD = 0.75   # from feature/early-warning
CRITICAL_THRESHOLD = 0.90  # from feature/critical-alert
```

`budget_alert()` now checks the critical level first. I removed the markers, added a test for
each level, ran all 9 tests (all passed), then used `git add` and `git commit` to finish the
merge, with a commit message explaining the decision.

## 4. What I learned about distributed version control
- **Branches make parallel work safe:** features stayed isolated and `main` always worked.
- **Conflicts are questions, not errors:** Git merges what it can and stops only where
  judgement is needed; `git status` and `git diff` show exactly where.
- **Resolving is a design decision:** understanding both intentions gave a better result than
  picking a side.
- **Tests make a resolution trustworthy**, and small, clear commits keep history readable.
- **Every clone is a full repository:** all of this happened offline; GitHub was only needed to
  share it. Pulling often and keeping branches short-lived reduces conflicts in a team.

Screenshots of each step are in the appendix and in `docs/screenshots`; full command output is
in `docs/evidence`.

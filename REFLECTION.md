# Reflection: Git and GitHub Project with an Intentional Merge Conflict

**Repository:** https://github.com/hharshitarajoria/expense-tracker

## 1. The project
I built a small command-line **Expense Tracker** in Python. A user can add expenses
(amount, category, date, note), list them, see totals by category and month, and set a
monthly budget that alerts them when spending gets close to the limit. The code is
deliberately small so the focus stays on Git: there are no third-party packages, data is
saved to JSON files, and nine unit tests check the main behaviour.

## 2. Workflow I followed
1. **`git init`** created the repository, and the first commit added a README and a
   `.gitignore` (so data files and `__pycache__` are never committed).
2. Every feature was built on its **own branch**, committed with a clear message, and merged
   into `main` with `git merge --no-ff`, so the history graph shows each feature separately:
   - `feature/add-list`: add and list expenses, with validation of amount and date
   - `feature/summary`: totals by category and month
   - `feature/budget-alert`: monthly budget, one alert at 80%, and unit tests
3. The repository was published on GitHub with **`git remote add`** and **`git push`**.

Commands used throughout: `git init`, `git status`, `git add`, `git commit`,
`git branch`/`git checkout -b`, `git diff`, `git merge`, `git log --oneline --graph`,
`git remote`, `git push`.

## 3. Creating the merge conflict
From the same commit on `main` I created two branches that disagreed about the budget alert:

| Branch | Change to `ALERT_THRESHOLD` | Change to the alert message |
|---|---|---|
| `feature/early-warning` | `0.80` → `0.75` | "WARNING … Consider slowing down." |
| `feature/critical-alert` | `0.80` → `0.90` | "CRITICAL … Only X left." |

Merging `feature/early-warning` into `main` succeeded because `main` had not changed since the
branch was made. When I then merged `feature/critical-alert`, Git reported:

```
CONFLICT (content): Merge conflict in expense_tracker.py
Automatic merge failed; fix conflicts and then commit the result.
```

**Why it happened:** Git merges line by line using the common ancestor. Both branches changed
the *same two lines* from the same original text in different ways. Git cannot know which
version is correct, so it stops and asks a person to decide. `git status` showed the file as
"both modified", and the file contained `<<<<<<< HEAD`, `=======` and `>>>>>>>` markers around
each disagreement.

## 4. How I resolved it
Picking one side would have thrown away the other developer's idea. The two branches were
really asking for different things: an early nudge and an urgent warning. So I kept both by
replacing the single threshold with two levels:

```python
WARNING_THRESHOLD = 0.75   # from feature/early-warning
CRITICAL_THRESHOLD = 0.90  # from feature/critical-alert
```

and checking the critical level first in `budget_alert()`. I removed all conflict markers,
added two new tests (one for each level), ran the full test suite (9 tests passed), then ran
`git add` and `git commit` to finish the merge. The merge commit message explains the decision
so that anyone reading the history later understands why the code looks this way.

## 5. What I learned about distributed version control
- **Branches make parallel work safe.** Each feature lived in isolation until it was ready,
  and `main` always held working code.
- **Conflicts are not errors; they are questions.** Git handles everything it can merge
  automatically and only stops where human judgement is needed. Reading `git status` and
  `git diff` calmly tells you exactly where to look.
- **Resolving a conflict is a design decision**, not just deleting markers. Talking to (or
  thinking like) the other developer often gives a better result than choosing one side.
- **Tests make resolution trustworthy.** Running the tests after the merge proved the combined
  code still worked.
- **Small, well-described commits** made the history easy to read, and `git log --graph`
  showed exactly where branches split and joined.
- **Every clone is a full copy.** All of this work, including the conflict, happened locally
  without a network; GitHub was only needed to share the finished history. In a team, pulling
  often (`git pull`) and keeping branches short-lived reduces the chance of conflicts.

## 6. Evidence
Screenshots are in [`docs/screenshots`](docs/screenshots) and the full command output is in
[`docs/evidence`](docs/evidence).

| Screenshot | Shows |
|---|---|
| `01-init-and-first-commit.png` | `git init` and the first commit |
| `02-feature-branch-add-list.png` | First feature branch, testing and commit |
| `03a-summary-feature.png`, `03b-budget-alert-feature.png` | Further features and unit tests |
| `04-two-conflicting-branches.png` | The two branches editing the same lines (`git diff`) |
| `05-merge-conflict-status.png` | The conflict: merge output, `git status`, `git diff` |
| `06-conflict-markers.png` | Conflict markers inside `expense_tracker.py` |
| `07-resolution-tests-and-commit.png` | Tests passing, `git add` and the merge commit |
| `08-history-graph.png` | `git log --graph` after resolution |
| `09-push-to-github.png` | `git remote add` and `git push` |
| `10-github-repo.png`, `11-github-branches.png` | The repository and all branches on GitHub |

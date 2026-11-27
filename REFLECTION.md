# Reflection: Git and GitHub Project with an Intentional Merge Conflict

**Repository:** https://github.com/hharshitarajoria/expense-tracker

## What caused the conflict

I created the conflict on purpose to see how Git behaves when two lines of work disagree. From the same commit on `main`, `feature/early-warning` lowered the budget alert threshold from 80% to 75%, while `feature/critical-alert` raised it to 90%. Each branch also rewrote the alert message. Either change on its own was valid, and the first one merged cleanly. The problem appeared only when the second branch tried to change lines that `main` had already changed. Git merges by comparing each side with the common ancestor. When only one side has changed a line, Git takes that change automatically. When both sides have changed it differently, there is no safe automatic answer, so Git stops and asks the developer to decide.

This showed me that a conflict is about overlapping edits, not about two people working on the same file. Git had merged my earlier feature branches without any help, even though they all touched `expense_tracker.py`.

## How I resolved it

I began with `git status`, which named the affected file, and `git diff`, which showed both versions side by side between conflict markers. Looking at the markers alone, the easiest option was to delete one side. I decided against that after asking what each branch was trying to achieve. One wanted to warn the user early enough to change their behaviour; the other wanted to avoid alarming them until the situation was serious. These goals do not exclude each other. I replaced the single threshold with a warning level at 75% and a critical level at 90%, and placed the critical check first so that it takes priority.

Removing the markers does not prove that the merged program is correct. I added a test for each new level and ran the whole suite before staging the file. All nine tests passed. I then used `git add` to mark the conflict as resolved and wrote a commit message recording what conflicted and why I kept both features, so that someone reading the history later can understand the decision.

## What I learned about distributed version control

- **Every clone is a complete repository.** I could branch, commit, merge and resolve the conflict on my own computer without any connection. GitHub was needed only to share the work.
- **Committing and sharing are separate steps.** `git commit` records history locally; `git push` publishes it. `git pull` brings in other people's commits by fetching them and then merging, which means a pull can also produce a conflict.
- **Branches make parallel work safe.** Unfinished ideas stayed away from `main`, and two competing designs could exist at the same time until I was ready to combine them.
- **History is a form of communication.** Small commits with clear messages, and explicit merge commits, made it easy to see where each change came from. The commit graph shows the two branches splitting and joining again.
- **Prevention is cheaper than resolution.** In a team I would pull often, keep branches short-lived, make focused commits and talk to a teammate before changing shared constants or functions.

Overall, I now see a merge conflict as a normal part of collaboration. Git handles the mechanical work, but the developer is still responsible for understanding both changes, choosing a result that makes sense and checking that it works. If I repeated the project, I would enable the three-way (diff3) conflict style from the start, because seeing the original line next to both new versions makes each side's intention much clearer.

Screenshots are in [docs/screenshots](docs/screenshots); recorded command output is in docs/evidence.

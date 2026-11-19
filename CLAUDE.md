# Instructions for Claude Code

Read these at the start of every session, in this order:

1. `PROJECT_BRIEF.md`: the single source of truth for this project.
2. `PROGRESS.md`: what is finished, open questions, and the next step.

Rules that matter most:

- Work one phase and one step at a time. After each step, stop and show what changed, how to check it, and the next step.
- Ask, don't guess. Never delete anything without an explicit "yes".
- Every commit and push is authored by the owner only. Never add "Co-Authored-By: Claude", "Generated with Claude Code" or any other AI name or attribution to commit messages, PR descriptions, files or code comments.
- Never commit or push unless asked. Before any commit or push, run the pre-push checklist in `PROJECT_BRIEF.md` section 9.
- Only one GitHub Actions workflow for now: `.github/workflows/pages.yml`, which publishes the site (switched on by the owner on 2026-11-19). No others until Phase 9.
- Never put secrets, personal emails, personal paths or employer material in any file, including `PROGRESS.md`.
- After every finished step, add an entry to `PROGRESS.md`.

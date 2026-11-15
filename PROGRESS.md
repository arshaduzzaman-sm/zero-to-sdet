# Progress log

Newest entry first. No secrets or personal data in this file.

---

## Decisions (section 14 and owner instructions)

| Decision | Value | Date |
| --- | --- | --- |
| Old repositories | Not touched. All work happens only in `zero-to-sdet`. Step 0.2 is skipped by the owner's choice. | 2026-11-15 |
| Commit authorship | Every commit and push is under the owner's name only (`Arshaduzzaman SM`, GitHub no-reply email). No AI names or co-author lines anywhere. | 2026-11-15 |
| UI automation tool | Playwright only. No Selenium. | 2026-11-15 |
| Python version | 3.13 (managed with uv) | 2026-11-15 |
| Main color | Calm blue | 2026-11-15 |
| BDD tool | Both behave and pytest-bdd, equal depth. No main track. | 2026-11-15 |
| Equal depth | Every topic and every tool is taught in full: playbook, lessons, templates with tests, Bug Hunt. No "main" vs "side" topics. Goal: a reader can reach senior/lead SDET level from this repo alone. | 2026-11-15 |
| Skills gaps | All 4 new topics and 13 new lessons from step 0.6 approved and added to brief section 11 (now 62 topics). | 2026-11-15 |
| Multi-database set | MySQL, PostgreSQL, SQLite, MongoDB | 2026-11-15 |
| Custom domain | GitHub Pages first | 2026-11-15 |
| Analytics | GoatCounter (account in Phase 9) | 2026-11-15 |

Step 0.4 is complete: every decision in brief section 14 is decided.

---

## 2026-11-15 · Phase 0 · Step 0.6: skills matrix (done)

Update: owner approved all gaps and chose equal depth for everything. Brief updated: core idea 3 ("Equal depth"), section 11 (62 topics, additions marked "added 0.6"), Phase 2 (Python for testers, Static testing), Phase 6 order (Testing microservices, Data and ETL testing), section 14 (BDD), rule 7.7 (tools with their own runner). The "Open questions" below are resolved.

**Done**

- Read 58 open QA/SDET job ads (7 junior, 15 mid, 23 senior, 13 lead) from about 12 countries, via public Greenhouse, Lever and Ashby job-board APIs plus 4 ads read by hand.
- Counted skill mentions with a keyword script. Read the ISTQB CTFL v4.0 and CTAL-TAE v2.0 syllabus chapter lists.
- Wrote `docs/start-here/skills-matrix.md`: 95 checklist skills by level, each linked to its lesson, with "in X% of ads" and the full list of ads.
- Saved the research scripts in `scripts/research/` (standard library only) so the check can be repeated.
- Key numbers: API testing 79%, CI/CD 75%, Python 70%, framework design 70%, SQL 56%, Playwright 53%, TypeScript/JavaScript 46%, Java 43%, AI tools/testing 43%, pytest 36%, Selenium 34%, BDD only 5%.
- BDD tools: behave named in 2 ads, pytest-bdd in 0.
- Performance tools: JMeter 11 ads, k6 9, Locust 2.

**Gaps found** (marked "(new)" on the page; not yet added to the catalog in the brief)

New topics: Python for testers; Static testing and reviews; Data and ETL testing; Testing microservices.
New lessons: testing principles and test process; non-functional test types; SDLC models; white-box coverage; checklist-based testing; TDD and ATDD; k6/JMeter overview; choosing an automation tool; verifying the test framework; keyword-driven testing and Robot Framework; regulated industries (HIPAA, PCI DSS, GDPR, SOC 2); continuous improvement of automation; which languages job ads ask for (TypeScript, Java).

**Files changed**

`docs/start-here/skills-matrix.md`, `scripts/research/fetch_job_ads.py`, `scripts/research/count_job_ad_skills.py`, `PROGRESS.md`

**Open questions**

- Approve the gaps, so they can be added to the catalog (brief section 11).
- BDD main track: behave (job ads) or pytest-bdd (brief rule 7.7: pytest is the base for all templates).

**Next step**

Owner approves gaps and the BDD choice. Then the Phase 0 gate check and the first commit (when asked).

---

## 2026-11-15 · Phase 0 · Step 0.5 (in progress): new repository setup

**Done**

- New private repository `zero-to-sdet` exists on GitHub (empty, fresh history). Description set.
- Local git repository started on branch `main`, remote `origin` set. Commit email is the GitHub no-reply address.
- Added `.gitignore` (secrets, Python, tests and reports, databases, Docker data, site build, OS and IDE files).
- Added `.pre-commit-config.yaml` with gitleaks v8.30.1 and basic safety hooks.
- Added `.python-version` (3.13), `CLAUDE.md`, `PROGRESS.md`, `PROJECT_BRIEF.md`.
- GitHub topics set from section 1 of the brief.
- No files copied from the old practice repo (decided in 0.1: lesson ideas only, rewritten later).

**Files changed**

`.gitignore`, `.pre-commit-config.yaml`, `.python-version`, `CLAUDE.md`, `PROGRESS.md`, `PROJECT_BRIEF.md`

**Open questions**

- Change the local MySQL `root` password (brief, section 9).
- Python 3.13, uv, pre-commit and gitleaks still need installing on the owner's machine (installer was not run by the assistant).

**Next step**

Owner installs the tools, then runs `pre-commit install` and the first gitleaks scan. Then step 0.4 (open decisions) and 0.6 (skills matrix).

---

## 2026-11-15 · Phase 0 · Step 0.1: inventory of the old repository

**Done**

- Inventoried all 18 files in the old practice repository plus 5 uncommitted local files.
- Decision: copy no code. The lessons follow a third-party course and call third-party servers. Their topics become lesson ideas for Phase 3 (API, database, BDD), rewritten against the Practice App.
- Secret scan of the old repo history: no passwords or keys found. Personal emails appear as commit authors in its history.

**Next step**

Step 0.2 and 0.5.

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
| Skills gaps | All 4 new topics and 13 new lessons from step 0.6 approved and added to brief section 11 (now 64 topics: 60 learning topics + 4 Toolbox pages). | 2026-11-15 |
| Multi-database set | MySQL, PostgreSQL, SQLite, MongoDB | 2026-11-15 |
| Custom domain | GitHub Pages first | 2026-11-15 |
| Analytics | GoatCounter (account in Phase 9) | 2026-11-15 |
| Way of working | Owner asked for best practice and security first, handled end to end ("complete the project"). Assistant installs tools, commits and pushes to the private repo after the pre-push checklist passes, and keeps going step by step, logging each step here. | 2026-11-15 |
| Dependencies | Pinned with SHA-256 hashes (`uv pip compile --generate-hashes`), installed with `--require-hashes`. | 2026-11-15 |
| Fonts | No external fonts (`font = false`): system fonts, no Google requests. | 2026-11-15 |

Step 0.4 is complete: every decision in brief section 14 is decided.

---

## 2026-11-15 · Phase 1 · Navigation for scale, part B: menu and overviews built from front matter

**Done**

- `scripts/build_nav.py` builds the menu (`nav` in `zensical.toml`) and the topic cards on every section overview page from each page's own front matter: `nav_title`, `order`, `group` (optional), `summary`, plus `level` and `status` for the card labels. Lessons inside a topic folder are picked up automatically.
- Adding a topic now means: make the folder and `index.md` with those fields, run the script. No hand-written list anywhere.
- One-off migration added the fields to all 70 pages from the old menu. Verified: same 74 menu entries, same labels.
- Groups in the four big sections (Core Automation, Infrastructure, Advanced Testing, Professional SDET). The breadcrumb skips group names (`extra.nav_groups`, written by the script; a group may not share a name with a page).
- Section overview pages: one card per topic (whole card clickable, level and "Coming soon" as text labels, small lift on hover, none with reduced motion).
- Pre-commit hook `build-nav` runs `build_nav.py --check`. Tested: a changed label without regenerating fails, a missing `summary` fails with a clear message.
- Bug found and fixed: the theme treated the first topic of a group as the group's own page (topics vanished from the sidebar). Topics inside groups are now one-page sections.

**How to check**

Open http://127.0.0.1:8001/zero-to-sdet/core-automation/ and http://127.0.0.1:8001/zero-to-sdet/advanced-testing/: grouped sidebar, cards per group, breadcrumb "Home > Core Automation > API testing" on a topic.

**Next step**

Step 1.10: repository documents. Add "how to add a topic" (the front matter fields above) to CONTRIBUTING.md.

---

## 2026-11-15 · Phase 1 · Navigation for scale, part A (owner request: professional UI that stays clean at 2000+ topics)

**Done**

- Rule: the top tabs never grow. Only the seven learning sections, in Learning Path order (Infrastructure now before Advanced Testing). "The Professional SDET" tab shortened to "Professional SDET". New topics always go inside a section.
- Home is reached by the logo and the breadcrumb ("Home > Section > Topic", `overrides/partials/path.html`). About, Changelog, Privacy and GitHub moved to the footer (`overrides/partials/copyright.html`).
- `navigation.prune`: each page carries only its own section's menu. Measured: 94 links / 66 KB per page before, 20 links / 37 KB after; stays flat as topics grow.
- Sidebar: unfinished topics show a small "Soon" text label instead of an icon.
- Top of page: only the Edit button (the "view source" button removed).
- End of page: feedback and author share one row (`overrides/partials/content.html`), wraps on phones.
- Top tabs restyled (owner request): soft rounded hover background, active tab in brand blue with a bar that grows from the centre, keyboard focus outline, no motion with reduced-motion.
- Checked in light, dark and narrow screenshots.

**Next step**

Part B: menu and section overview pages built by a script from each topic's front matter (order, group, level, status), so adding a topic never means editing a hand-written list.

---

## 2026-11-15 · Phase 1 · Step 1.8: "Was this page helpful?" and comments template

**Done**

- "Was this page helpful?" with 👍/👎 at the end of every finished page (not on drafts or the home page). A click locks the buttons, keeps the chosen one blue, and shows a thank-you note. 👎 links to a new GitHub issue with the page title and address filled in.
- Own analytics provider `overrides/partials/integrations/analytics/goatcounter.html`: today it loads nothing from other sites and sends nothing. In Phase 9, once GoatCounter's script is added (pinned, with integrity hash), clicks are also counted as events.
- `overrides/partials/feedback.html`: theme partial plus draft hiding and a screen-reader status note.
- Giscus comments template `overrides/partials/comments.html`, switched off (`[project.extra.giscus] enabled = false`). Needs a public repo; follows the light/dark switch.
- Bug found and fixed in testing: the click script ran before the theme's script loaded; now it waits for the page to load.

**How to check**

Open http://127.0.0.1:8001/zero-to-sdet/learning-path/, scroll to the bottom, click 👍 or 👎. Draft pages (for example API testing) show no widget.

**Phase 9 to-do**

- Add GoatCounter count.js (pinned version, integrity hash) and update the About privacy section.
- Turn on Discussions, get `repo_id` and `category_id` from giscus.app, set `enabled = true`, mention giscus.app in the privacy section.

**Next step**

Step 1.10: repository documents (STYLE_GUIDE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE, issue and PR templates). Step 1.9 (Discussions) waits for the public repo.

---

## 2026-11-15 · Phase 1 · Step 1.7: About page and author line

**Done**

- New About page: what the site is, why it exists, licences (MIT code, CC BY 4.0 text), privacy (no cookies, self-hosted fonts), how to help.
- Author card with GitHub and LinkedIn links. Photo and short bio are left as marked comments in `docs/about.md` until the owner provides them (nothing invented).
- Every page now ends with "Written by Arshaduzzaman SM." (links to About) via `overrides/partials/source-file.html`. Home hides it with `hide: [author]`.
- Owner decision: no visible "Last updated" date (an old date makes a correct lesson look abandoned). The date (`updated: YYYY-MM-DD`, filled from git history by `scripts/update_page_dates.py`, drafts skipped) goes only into a hidden `article:modified_time` meta tag via `overrides/main.html`.
- Planned instead: a "Tested with" line (tool versions) on every real lesson, from Phase 2. New items go in the Changelog.

**How to check**

Open http://127.0.0.1:8001/zero-to-sdet/about/ and scroll to the bottom of any finished page (for example the Learning Path). `zensical build --strict` passes.

**Open questions**

- Owner photo (optional, square, metadata removed) and a 2–3 line bio for the About page.

**Next step**

Step 1.8: "Was this page helpful?" widget and the Giscus comments template (switched on in Phase 9).

---

## 2026-11-15 · Phase 1 · Design pass (owner request: more attractive, beautiful diagrams, perfect text, click animations)

**Design system**

- Colours: harbor blue `#1f5fbf`, deep navy dark mode `#0f1a2b` (not plain black), mist surface `#eef3fa`, ink text `#16243a`, pass green and fail red used only for test results.
- Font: Atkinson Hyperlegible Next + Mono (Braille Institute, made for legibility; OFL 1.1). Self-hosted in `docs/assets/fonts/` from the official @fontsource npm packages 5.3.0, sha512 integrity verified. About 73 KB. No requests to Google.
- One memorable element: the home hero runs a pytest session once (6 tests pass). Motion otherwise only answers the reader: button press, row press, folded blocks sliding open. All motion stops under "reduce motion".
- Home: hero (words left, terminal right), "I need to…" as compact rows with icon chips (whole row clickable, focus ring for keyboard), role paths 2 x 2, the six stages as a real numbered route, comfortable line length.
- Diagrams: rounded nodes, wide text, brand colours, self-hosted font (Mermaid options per diagram; the theme's shadow DOM blocks outside CSS).
- Info boxes use the same easy text size as the body. Footer text without dot separators.
- Checked with screenshots in light and dark mode.

**Files changed**

`docs/assets/stylesheets/extra.css`, `docs/assets/fonts/*`, `docs/index.md`, `docs/learning-path.md`, `zensical.toml`

**Next step**

1.7 About page and footer with the author name (waiting for optional photo and short bio from the owner).

---

## 2026-11-15 · Phase 1 · Steps 1.5 and 1.6: Home page and Learning Path

**Done**

- 1.5 Home page (`docs/index.md`): hero with promise, tagline, "Start learning" and "Star on GitHub" buttons; "What is an SDET?" in plain words; "I need to…" finder with 12 task cards (whole card clickable); "Pick your path" (4 role paths, 2 x 2); cards for every area; "How every lesson works"; star call to action.
- 1.6 Learning Path (`docs/learning-path.md`): plain-words box, a straight top-to-bottom Mermaid map with the level reached after each stage, and four ordered paths: manual tester to automation, junior to mid, mid to senior, interview prep in 4 weeks.
- `docs/assets/stylesheets/extra.css`: comfortable text size, hero, card hover, centred diagrams, 2-column path cards, no edit buttons over the home hero, phone padding.
- Checked with screenshots at desktop and 600 px width. All 44 icons render. Strict build clean.

**Owner instruction (standing):** keep the UI beginner-friendly; every lesson must be learnable step by step; finish gradually.

**Note**

- Headless Chrome cannot render narrower than about 500 px, so a real phone-width check (390 px) is added with Playwright device emulation in Phase 3.

**Next step**

1.7 About page and footer with the author name.

---

## 2026-11-15 · Phase 1 · Steps 1.1 to 1.4: skeleton, Zensical config, Markdown features, local preview

**Done**

- 1.1 Folder skeleton generated from brief section 11: a placeholder page for each of the 63 topic folders (Glossary is a single page), 7 tab overview pages, plus Home, Learning Path, About, Glossary, Tags, Changelog. Each placeholder lists the lessons and templates it will contain. `docs/assets/images/IMAGES_NEEDED.md`, `docs/assets/diagrams/`, `modules/README.md`.
- 1.2 Zensical 0.1.1 installed in `.venv` (Python 3.13). `zensical.toml`: name, URL, author, copyright, repo link with "Edit this page", tabs, breadcrumbs, search highlight, instant navigation, back-to-top, previous/next footer, calm blue light/dark/system palettes, GitHub and LinkedIn links.
- 1.3 Markdown features: admonitions, details (collapsible), tabs, Mermaid, task lists, snippets (base path = repo root, missing files fail the build), tags plugin with index on `tags.md`, a "Coming soon" status badge for draft pages.
- 1.4 `zensical build --strict`: no issues. `zensical serve` serves every page (HTTP 200).

**How to check**

```bash
cd ~/Documents/"Claude code"/zero-to-sdet
.venv/bin/zensical serve
# open http://127.0.0.1:8001/zero-to-sdet/
# (port 8001 is set in zensical.toml; port 8000 is used by another local project)
```

**Files changed**

`zensical.toml`, `requirements-docs.in`, `requirements-docs.txt`, `docs/**` (placeholder pages), `modules/README.md`, `PROJECT_BRIEF.md` (topic count corrected to 64), `PROGRESS.md`

**Notes for later**

- The theme loads Mermaid from unpkg.com on pages that have a diagram. Review in Phase 9 (self-host for privacy).
- The level badge, Giscus comments and the feedback widget need template overrides: steps 1.8 and 1.15.
- Giscus needs a public repo with Discussions, so it can only go live in Phase 9. Its template is prepared earlier.

**Next step**

1.5 Home page: hero, "I need to…" task finder, learning paths by role, pillar cards, star button.

---

## 2026-11-15 · Phase 0 · Gate passed

**Done**

- Tools installed on the owner's machine (owner authorized): uv 0.13.8, Python 3.13.18 (via uv), pre-commit 4.7.0 (via `uv tool`), gitleaks 8.30.1 (official GitHub release, SHA-256 checksum verified, in `~/.local/bin`).
- `pre-commit install` done; all hooks pass on every file.
- Pre-push checklist passed: gitleaks clean (staged and full history), no personal paths or emails, no images, no `.env`, no third-party course material.
- First commit `06baf46` pushed to the private `zero-to-sdet` repo. Author: Arshaduzzaman SM (no-reply email). No AI attribution.

**Gate check**

- Clean `main`: yes. No secrets: yes. Decisions written down: yes.

**Note for the Phase 9 audit**

- `PROJECT_BRIEF.md` mentions that an old private repo once held a real password. Harmless, but decide before going public whether the brief should be public as is.

**Next step**

Phase 1, step 1.1: folder skeleton with placeholder pages for every tab.

---

## 2026-11-15 · Phase 0 · Step 0.6: skills matrix (done)

Update: owner approved all gaps and chose equal depth for everything. Brief updated: core idea 3 ("Equal depth"), section 11 (64 topics, additions marked "added 0.6"), Phase 2 (Python for testers, Static testing), Phase 6 order (Testing microservices, Data and ETL testing), section 14 (BDD), rule 7.7 (tools with their own runner). The "Open questions" below are resolved.

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

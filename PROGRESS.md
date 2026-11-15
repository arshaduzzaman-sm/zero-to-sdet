# Progress log

Newest entry first. No secrets or personal data in this file.

---

## Decisions (section 14 and owner instructions)

| Decision | Value | Date |
| --- | --- | --- |
| Old repositories | Not touched. All work happens only in `zero-to-sdet`. Step 0.2 is skipped by the owner's choice. | 2026-11-15 |
| Commit authorship | Every commit and push is under the owner's name only (`Arshaduzzaman SM`, GitHub no-reply email). No AI names or co-author lines anywhere. | 2026-11-15 |
| UI automation tool | Playwright only. No Selenium. | 2026-11-15 |
| Practice App online | GitHub Codespaces only: each learner gets a private copy of the whole app (added in step 1.5.6). No shared public hosting; no browser-only demo on GitHub Pages. Pages hosts only the lesson site. | 2026-11-15 |
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
| Page dates | No visible "last updated" date; hidden meta tag only. Lessons show "Tested with" versions instead. | 2026-11-15 |
| Navigation | Seven fixed tabs; menu and section overviews generated from page front matter by `scripts/build_nav.py`. | 2026-11-15 |
| Readability tool | pyphen + own Flesch-Kincaid formula instead of textstat (textstat pulls in nltk and 7 more packages; fewer dependencies is safer). | 2026-11-15 |
| Share images | Own script with Pillow (owner approved): made at build time into site/, cached, never committed. Zensical cannot make them yet. | 2026-11-15 |
| Code of Conduct contact | LinkedIn for now; discussed again in Phase 9 (owner may create a project email). | 2026-11-15 |
| Focus: lessons first | The site and its lessons are the main product; the Practice App is a helper. Finish Phase 1.5 small (starter set of about 6 planted bugs, one short tour page), then build lessons. After that the app only changes when a lesson needs it. Every lesson must teach fully from the page alone, with real output or a screenshot after every step, for readers who never run the app. | 2026-11-15 |
| Pillar 6: AI-Powered QA | Owner added a new pillar of 11 topics (brief section 11 and Phase 7.5). Saved now, built later. The Pillar 3 topic "AI in testing" moves into it as "Testing AI features". Templates use a fake model in tests (offline, no key, no cost). AI provider for examples: decide when the phase starts. | 2026-11-15 |
| Pages are the whole product | The app is no longer a focus (readers would have to download and run it). Lessons use real job situations and show every output on the page; the Practice App is only an optional "try it" box. Every page must help someone who has never tested, an engineer stuck on a task, and an experienced engineer. | 2026-11-16 |
| Real templates only | Templates are the scripts, code snippets, checklists and plans people use at work, ready to adapt. No toy exercises (the skills self-assessment CSV and score script are to be removed, owner said yes). | 2026-11-16 |
| No level talk | No "zero to mid level", "junior to mid-level", "first test to senior level" anywhere. The Skills Matrix is grouped by area. | 2026-11-16 |
| Author's note | Home (short) and About (full): the content comes from the author's work and from what many people shared online, gathered in one place in plain words, with thanks. | 2026-11-16 |
| No story characters | Pages talk straight to the reader, like a senior engineer explaining real work ("Your lead asks…", "Ask the product owner…"). No named hero whose day the reader follows. Arshad stays only as a test-data name. Style guide and brief section 8 updated. | 2026-11-16 |
| coverage.py | Added to `requirements.txt` (7.17.3, pinned with hashes) for the statement and branch coverage lesson. Owner said yes. Nothing else changed in the lock file. | 2026-11-16 |

Step 0.4 is complete: every decision in brief section 14 is decided.

---

## 2026-11-16 · Phase 2 · Topic 4 complete: statement and branch coverage

**Done**

- Owner approved `coverage`. Added to `requirements.in` and compiled with hashes (coverage 7.17.3 only; no other package changed). Installed with `--require-hashes`.
- Lesson "Statement and branch coverage", with a real demo: a points rule has 100% line coverage, but branch coverage shows 80% with the "not a member" path never taken. One test for that path finds a crash (`UnboundLocalError`) that every non-member customer would have hit. After the fix, branches are 100%. The lesson also shows what coverage can't tell you (mixes of conditions, missing code), and a `fail_under` limit.
- New template: `.coveragerc` (branches on, missing lines shown, `fail_under`).
- 50 topic tests (was 45): the demo's numbers, the crash and the fix are all checked.
- 3 new glossary terms: statement coverage, branch coverage, white-box testing.
- Topic 4 now has all nine lessons from the brief.

**Check it**

`bash scripts/check.sh` passes. Page: Test design techniques, then Statement and branch coverage.

**Next step**

Topic 5: Static testing and reviews.

---

## 2026-11-16 · Phase 2 · Topic 4, part B: four more techniques

**Done**

- Four lessons, written straight to the reader, each with "When it goes wrong":
  - pairwise testing: 36 checkout combinations cut to 9 that cover every pair, with NIST's research on why pairs are enough;
  - error guessing: a probe of tricky usernames found two real problems in the example rule. "José" is accepted but the Bengali name "আরশাদ" is refused (Python doesn't count the vowel sign "া" as a letter), and wide letters that look like "admin" are accepted. The lesson shows how to raise these as questions before writing tests;
  - exploratory testing: a charter, a time box, and real session notes on order cancelling (found a misleading message for unknown actions);
  - checklist-based testing: ready-to-use web form and API endpoint checklists, and how to keep them short.
- New templates: `pairwise.py` (no extra packages), error guessing checklist, exploratory charter, web form checklist, API endpoint checklist. Plus an example session and a probe script.
- 45 topic tests (was 27): pairwise covers every pair, the probe shows both open questions, every checklist has its sections.
- 4 new glossary terms. "Exploratory testing" now points to its lesson.

**Check it**

`bash scripts/check.sh` passes. Pages: Think like a tester, then Test design techniques.

**Next step**

Last lesson of Topic 4: statement and branch coverage. It needs the `coverage` package; waiting for the owner's yes.

---

## 2026-11-16 · Phase 2 · Voice: no story characters (owner request)

**Done**

- Owner said the "Arshad's lead asks him…" stories feel cartoon-like and would look childish on a public repo. Pages should explain practically, like a senior engineer, in easy words.
- Rewrote every story line in Topics 1 to 4 (21 files) to talk straight to the reader: "You test an online shop. Your lead says…", "Ask the product owner…". The worked examples, outputs and steps are unchanged.
- "Maria" as a teammate is gone too ("a developer on the team"). Arshad stays only as test data (the test user in emails and in code), as the brief says.
- STYLE_GUIDE.md and PROJECT_BRIEF.md section 8 now say: no story characters.

**Next step**

Topic 4, part B (waiting on the owner's answer about the `coverage` package).

---

## 2026-11-16 · Phase 2 · Topic 4, part A: Test design techniques

**Done**

- Playbook page: Arshad has two days to test a member launch (sign-up form, delivery fees, order cancelling). He picks a technique for each kind of rule and finds a missing rule (is express free for big orders?) before writing code.
- Four lessons, each with a "When it goes wrong" section: equivalence partitioning, boundary values, decision tables, state transitions.
- Every lesson shows a real bug its technique catches:
  - an off-by-one age check that group tests miss and an edge test catches;
  - a forgotten member rule caught by row 4 of the decision table;
  - a "cancel after shipping" move caught by the refused-move tests.
- Real templates: three worksheets, `boundaries.py` (lists edge values), `decision_table.py` (prints the empty table). 27 topic tests check the templates, and that each lesson's bug is really caught.
- Found while writing: a state test that copies the code's own table can't catch a wrong table. The example test keeps its own list, and the lesson teaches this. Also, `$50` inside double quotes disappears in the shell, so the commands use single quotes.
- 4 new glossary terms, and 2 existing terms now point to their lessons.

**Check it**

`bash scripts/check.sh` passes. Pages: Think like a tester, then Test design techniques.

**Next step**

Topic 4, part B: pairwise, error guessing, exploratory testing, checklist-based testing, and statement and branch coverage. The coverage lesson needs the `coverage` package, which is not installed yet: ask the owner first.

---

## 2026-11-16 · Phase 2 · Topic 3: Test levels and the pyramid

**Done**

- Playbook page: Arshad's team has a slow, flaky suite. He measures its shape (an "ice cream cone"), moves rule checks down a level, and reports the result. It includes "Stuck? Try this" and an optional Bug Hunt box (BH-01).
- Five lessons, in a teacher's voice, each with a "When it goes wrong" section:
  - the test levels: one small shop tested at every level, including an integration test catching a bug that seven unit tests missed;
  - the test pyramid: the ice cream cone, and how to move a test down safely;
  - the testing trophy: a real Ruff example of static analysis;
  - non-functional testing: a first speed check, and why percentiles beat averages;
  - choosing the right level: a five-question decision chart, worked through on a coupon feature.
- Real templates: `pytest.ini` with the levels, a `conftest.py` that marks tests by folder, a pyramid report script, and a decision chart. The example shop has unit, integration, API and UI tests plus a speed check. 14 tests cover the templates and examples.
- Every output on the pages is real, from real runs.
- 8 new glossary terms: test level, API test, ice cream cone, marker, testing trophy, static analysis, non-functional testing, percentile.

**Check it**

`bash scripts/check.sh` passes. Pages: Think like a tester, then Test levels and the pyramid.

**Next step**

Topic 4: Test design techniques.

---

## 2026-11-16 · Phase 2 · Topic 2 lessons: "When it goes wrong"

**Done**

- Each of the five Topic 2 lessons now has a "When it goes wrong" section, matching Topic 1 and lesson template step 7a. Examples: a test fails and you don't know why; "it works on my machine"; every skill looks like a gap; "is it bug-free?" before a release; the test environment is broken on execution day.

**Next step**

Topic 3: Test levels and the pyramid.

---

## 2026-11-16 · Phase 2 · Topic 1 rewritten in a teacher's voice

**Done**

- Owner asked for pages that read like a real teacher explaining with examples, in plain English (not stiff or "AI-sounding"), covering how to think and what to do when something goes wrong. This is saved as style guide and brief section 8B, and the lesson template gains a "When it goes wrong" section (7a).
- All seven Topic 1 pages are rewritten in that voice. Every lesson has a new "When it goes wrong" section, and the playbook gains "Stuck? Try this".
- Examples are now framed as Arshad's real work. The shop runs on his computer; on your team, it is your test environment. The Practice App appears only in the optional Bug Hunt box.
- The real outputs are kept.
- Arshad's example plan no longer depends on the app.
- New references: curl docs, Atlassian's definition of done, VS Code search, Docker compose. All links were checked.

**Next step**

Add "When it goes wrong" to the five Topic 2 lessons, then Topic 3: Test levels and the pyramid.

---

## 2026-11-16 · Phase 2 · Topic 2 rewritten: real job templates, no app needed

**Done**

- Removed (owner said yes): the skills self-assessment CSV, the score script, Arshad's example scores and their tests.
- New templates that SDETs really use, in `modules/think_like_a_tester/the_sdet_role/templates/`:
  - new team onboarding checklist (access, people, product, existing tests, first useful change);
  - 30-60-90 day plan (goals with proof, support needed, risks, check-ins);
  - automation readiness checklist (worth it, reliable, rough payback, decision);
  - a pytest smoke test for any app (`BASE_URL`, health check, speed, pages; standard library only; skips without `BASE_URL`).
- Example code for the lessons: a shipping rule and its boundary tests (`examples/`).
- 11 tests: credit line and sections of each checklist; the example passes; the smoke test passes on a healthy app, names a broken health check or a missing page, and skips without `BASE_URL` (run against a small local fake app).
- Pages rewritten around real work, with real output on the page and no app needed:
  - the playbook: first smoke test, choosing what to automate, the 90-day plan, and a new "Stuck? Try this" box;
  - what an SDET does: a test catching a `>=` changed to `>`;
  - SDET vs QA vs developer: one bug through three roles, with a pipeline file;
  - skills map: gaps tied to a real task, with no CSV;
  - principles: 4 tests pass while the bug is still there, and 46,800,000 checkout combinations;
  - test process: what `-k` really selected.
- The Practice App is now only an optional Bug Hunt box.
- The playbook standard (brief 7.1) and `_new_topic_template` now include "Stuck? Try this", and the Bug Hunt is optional.
- pytest no longer collects `templates/` and `examples/` directly. Topic tests run them the way a reader would. Ruff allows `assert` in test templates.

**Next step**

Rewrite Topic 1 (Learning a new testing area) the same way: real job examples, the app only optional. Then Topic 3, Test levels and the pyramid.

---

## 2026-11-16 · Owner direction: pages for everyone, real templates, author's note

**Done**

- Brief updated (sections 1, 2, 6, 7.1, 7.2, 7.3, 11): new tagline, readers without levels, the "for everyone", "real templates" and "author's note" decisions, and app examples made optional.
- Level words removed: tagline (site, README, banner, home), home paths ("Build a whole test suite", "Design how a team tests"), Learning Path (no "you are now a junior SDET" lines), Skills Matrix (95 skills regrouped into 12 areas, job ad table without a level column; the progress tracker now groups by area), the "Leading quality" and "Career roadmap" pages, the "Senior skills" menu group (now "Building and leading"), and the new-topic script.
- Author's note: short on Home ("Why I made this"), full on About.

**Next step**

Rewrite Topic 2 with real job templates (new team onboarding checklist, 30-60-90 day plan, automation readiness checklist) and remove the skills CSV and score script. Then rewrite Topic 1 the same way.

---

## 2026-11-16 · Phase 2 · Topic 2: The SDET role

**Done**

- Playbook page: Arshad, a manual tester, is asked to be the team's first SDET and plans his first 90 days through all nine steps. It has real outputs (the app's 177 tests, his skills score), "How an experienced SDET thinks", "Red flags", templates, a Bug Hunt (BH-05, the cart badge) and official resources.
- Five lessons on the lesson template:
  - what an SDET does (a real test catching the free shipping bug);
  - SDET vs QA vs developer (one bug, three roles, how to read a job ad);
  - skills map (the seven skill areas and the scoring script);
  - the seven testing principles (ISTQB CTFL v4.0, with real runs: the login tests pass while a reset bug exists, and the full suite catches only 3 of 6 planted bugs);
  - the test process and testware (the seven ISTQB activities, matched to the 9-step playbook).
- Template in `modules/think_like_a_tester/the_sdet_role/`: a skills self-assessment CSV, a scoring script (area scores, overall score, three skills to learn next), and Arshad's example. 11 tests.
- Practice App test fix: the app's tests now switch the planted bugs off for every test. Before, `test_money.py` failed when run on its own, because it never built the app. New setting `BOOKSHELF_TEST_BUGS=on` runs the app's tests with the bugs on, so readers can repeat the principles lesson. Documented in the app README and `conftest.py`.
- Glossary: 5 new terms (ISTQB, pesticide paradox, defect clustering, test condition, testware). Readability: grade 2.1 to 3.9.

**Open (definition of done)**

- Cheat sheet image per topic, and "read aloud once": same as Topic 1.

**Next step**

Topic 3: Test levels and the pyramid.

---

## 2026-11-15 · Phase 2 · Topic 1: Learning a new testing area

**Done**

- The first full topic. Its playbook page follows one realistic task (Arshad is asked to own password reset testing) through all nine steps, against the Practice App, with real outputs at every step. It includes "How an experienced SDET thinks", "Red flags", "Jump to what you need", templates, a Bug Hunt and official resources.
- Six lessons, each built on the lesson template (before you start, outcomes, why it matters at work, plain words and a diagram, step by step with real output, common mistakes, "if you see this error", try it yourself with a folded solution, quick check, references):
  - how to approach a task you have never done;
  - the 9-step playbook;
  - asking the right questions;
  - reading official docs fast;
  - learning from code and examples;
  - when to ask for help.
- Templates in `modules/think_like_a_tester/learning_a_new_testing_area/`: day-one questions, one-page test plan and learning log, plus Arshad's filled-in example plan. The pages pull them in from `modules/`, so the site always shows the tested files. 9 tests check the credit line, every section, and that the example fills the whole template.
- Bug Hunt: use the playbook on password reset. Its answer is BH-06, folded on the tour page.
- Every fact was checked against the real app while writing. Three were corrected: the 404 answer format, which tests exist for invoices (a lesson in "search before you call it a gap"), and a doubtful error example, replaced with one seen for real (`command not found: pytest`).
- Glossary: 6 new terms (happy path, negative test, edge case, scope, risk, playbook). Readability: grade 2.4 to 3.3 on every page.

**Open (definition of done)**

- One cheat sheet image per topic (brief 7.5): to make once a few topics are written, in one style for all.
- "Read aloud once": for the owner, when reviewing.

**Next step**

Topic 2: The SDET role.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.8: Practice App tour page, and the Phase 1.5 gate

**Done**

- The first finished page with real content: [Practice App tour](docs/start-here/practice-app-tour/index.md). It follows the lesson template: before you start, what you will learn, why it matters at work, an everyday comparison, a diagram of the parts, then seven steps (start, open the shop, status, API docs, emails, reset, stop), each with a screenshot or the real output. After that come the Bug Hunt hints with the six answers folded, common mistakes, "if you see this error", an exercise with a solution, a quick check, and references.
- Built for "learn from the page alone": a reader who installs nothing still sees every screen and every output.
- Four screenshots (shop, status, API docs, Mailpit), 14 to 47 KB each, without metadata, showing only fake data. The Mailpit screenshot is filtered to one `@example.com` address, so no other test email shows.
- gitleaks flagged two harmless example values on the page (a random request id and the start of a token). Both are now shortened, so the scan stays clean.
- The page passes the readability check (grade 8 or lower). The menu and README no longer mark it "coming soon".

**Phase 1.5 gate: one-command start on macOS, Windows and Linux**

- macOS: passed (`docker compose up -d`, all five parts healthy).
- Linux: the setup and all app tests pass in a clean Debian container; Codespaces itself runs on Linux.
- Windows and a real Codespace: not checked yet, because they need the owner's machine or account. Open items for the owner, at any time. Phase 2 starts now, as the owner asked ("lessons first").

**Next step**

Phase 2: Pillar 1, Think Like a Tester, starting with "Learning a new testing area".

---

## 2026-11-15 · Phase 1.5 · Step 1.5.7: starter set of planted bugs

**Done**

- Six bugs planted on purpose, one per area: business rule boundary (BH-01), API pagination (BH-02), reporting database (BH-03), access control / IDOR (BH-04), web page (BH-05), and time-based security (BH-06). Each one is a mistake real teams make, and each fits a lesson technique: boundary values, comparing two databases, changing ids, comparing web and API, or using the clock control.
- The switch: `PRACTICE_APP_BUGS=off` (in `.env` or docker compose) turns them all off; on by default. The code marks each bug only with its answer code, with no description in comments.
- Answers: `practice-app/BUG_HUNT_ANSWERS.md` gives each bug's steps, expected and actual result, the testing technique, and severity. The website gets them folded in step 1.5.8.
- Found while writing the answers: every seed price ends in .99, so no cart reaches exactly $50.00. BH-01's steps start with the admin making a $25.00 product, which is itself a lesson in making boundary test data.
- The bugs stay inside the local app: they never touch the repository, the site or CI.
- Tests: the app's own tests run with the bugs off; `test_planted_bugs.py` checks each bug both on and off (12 tests). 177 app tests pass. Checked live in Docker with the switch on and off.

**Next step**

Step 1.5.8: the Practice App tour page (finished, with the Bug Hunt answers folded).

---

## 2026-11-15 · Phase 1.5 · Step 1.5.6: one-command start, reset, status page, Codespaces, safety guard

**Done**

- **One command:** `cd practice-app && docker compose up -d` starts the shop, PostgreSQL, MySQL, MongoDB and Mailpit, in order and with health checks. Checked on macOS: all five healthy in 27 seconds after the first build, and email, uploads, invoices and reset all worked inside Docker. No `.env` is needed.
- **App image** (`practice-app/Dockerfile`): Python 3.13.18 slim, pinned by digest; packages installed with `--require-hashes`; runs as a normal user (uid 10001), never root. `.dockerignore` keeps `.env`, `data/` and tests out of the image. Data (uploads, outbox) lives in a named volume.
- **Reset:** `python -m bookshelf reset` (or `docker compose exec app python -m bookshelf reset`) puts every database back to the seed data and deletes uploaded pictures. Admin page and API reset still work.
- **Status page** `/status`: each part (shop and API, the three databases, email) with up, down or "in the terminal". It answers 503 when a part is down, like `/api/health`. The footer links to it.
- **Safety guard:** the app refuses to start on any address other than `127.0.0.1`, `localhost` or `::1` while it still uses fake values from `.env.example`, and says which ones. Inside Docker it must listen on `0.0.0.0`; that is allowed only with `CONTAINER_PORT_IS_LOCAL_ONLY=yes`, set in `docker-compose.yml` next to the `127.0.0.1` port.
- **GitHub Codespaces** (`.devcontainer/`): Python 3.13 dev image and the docker-in-docker feature 2.17.0, both pinned by digest. Packages are installed with hash checks; the app starts by itself; ports 8080 and 58025 are labelled and stay private. The "Open in GitHub Codespaces" button is in both READMEs. The setup script was tested on Linux in a clean Python 3.13 Debian container: everything installed and all app tests passed there.
- `.gitattributes`: shell scripts, the Dockerfile and `.devcontainer/` keep Unix line endings, even when cloned on Windows.
- Tests: 12 new (guard, reset command, status page). 166 app tests pass.
- Docs: Practice App README rewritten around the one-command start (Codespaces, without Docker, reset, safety); DESIGN.md (start, online, safety, folder layout); root README (Codespaces button, folder table).

**Not tested yet (needs the owner or later phases)**

- A real Codespace: the button only opens once someone with access clicks it, and it uses the owner's free Codespace hours. Worth one try by the owner; a Linux container check stood in for it.
- Windows: no Windows machine here. Docker Desktop runs the same Linux containers, so the risk is low; the Phase 1.5 gate needs one run on Windows.

**How to check**

`cd practice-app && docker compose up -d`, then open http://127.0.0.1:8080/status: every part should say Up. Try `HOST=0.0.0.0 ../.venv/bin/python -m bookshelf`: it refuses to start and says why.

**Next step**

Step 1.5.7: a starter set of about 6 planted bugs, the switch that turns them off, and the folded answers page.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.5: email, picture uploads, invoice PDF

**Done**

- **Email through Mailpit:** sign-up code, reset code and order confirmation go to Mailpit when `SMTP_HOST` is set. Read them at http://127.0.0.1:58025 or with Mailpit's API. Without it, emails are printed and saved in `data/outbox/` as before. A failed send is logged and never breaks the request. Mailpit 1.33.1 is in `docker-compose.yml`, pinned by digest, on 127.0.0.1 only (web 58025, SMTP 51025), with the update check and remote fonts turned off. `/api/health` now shows `email` (up, down, or console).
- **Picture uploads:** profile picture (`POST/DELETE /api/users/me/avatar`, `GET /api/users/{id}/avatar`, owner or admin only) and product image (`POST /api/products/{id}/image` admin, `GET` public). JPEG or PNG only, up to 2 MB and 25 million pixels. Pillow must open the file as a real picture: a renamed text file, a fake PNG header or a GIF is refused with a clear error. A clean copy is saved, turned upright, with no hidden metadata (GPS and camera details are removed), under a random name in `data/files/`. The path is checked so it can never leave that folder. Reset deletes all uploads.
- **Invoice PDF:** `GET /api/orders/{id}/invoice.pdf`, made on request with fpdf2 and never stored. Marked "Practice invoice ... Not a real document". Someone else's order gives 404; an unpaid order gives 409 `INVOICE_NOT_AVAILABLE`.
- **Web pages:** profile picture box on the profile page (upload, remove, errors next to the field), an image column on the admin page, product images on cards and the product page (a letter placeholder when there is none), and a "Download invoice (PDF)" button on the order page. Upload forms carry the CSRF token too, and every new element has a `data-testid`.
- **Older data:** if the database was made by an older app version (missing columns), the app rebuilds it from the seed on start and says so in the terminal, instead of crashing.
- Tests never touch the real `data/files/`: each test app gets its own temporary folder.
- Tests: 27 new (uploads, metadata removal, permissions, invoices, SMTP with a stand-in server, web forms, plus one that checks real Mailpit when `BOOKSHELF_TEST_MAILPIT` is set). All 155 app tests pass on SQLite and on Docker (PostgreSQL, MySQL, MongoDB and real Mailpit). Checked live too: a sign-up email arrived in Mailpit, an upload worked, and the invoice PDF opened correctly.
- New packages, checked on PyPI and pinned with hashes: fpdf2 (py-pdf), pillow (already used by the site scripts), fonttools (needed by fpdf2).
- DESIGN.md (email, files and invoice rules; ports; endpoints), README (emails, pictures and invoices) and `.env.example` (`SMTP_HOST`, `SMTP_PORT`) updated.

**How to check**

`cd practice-app && docker compose up -d mailpit`, then `SMTP_HOST=127.0.0.1 SMTP_PORT=51025 ../.venv/bin/python -m bookshelf`. Sign up on http://127.0.0.1:8080/signup and read the code at http://127.0.0.1:58025. Log in as `arshad`, add a profile picture on the profile page, and download the invoice of order 1.

**Next step**

Step 1.5.6: the app itself in docker compose (one-command start), reset script, status page, GitHub Codespaces setup with an "Open in Codespaces" button, and a guard that stops the app on a non-local address while it still uses the fake default passwords.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.4: web pages

**Done**

- The shop's web pages (`practice-app/bookshelf/web/`, `templates/`, `static/`): product list with search, category, price filters, sorting and pages; product page with add to cart and reviews; sign up, verify code, log in, log out, forgot and reset password; profile; cart with quantities, remove and coupons; checkout with the sandbox cards; my orders, order details and cancel; admin (stock, visibility, add product, ship and deliver orders, reporting sync, reset); friendly error pages. `/docs` stays the API page.
- Built on the same functions as the API, so web and API follow the same rules (and later the same planted bugs).
- Test hooks: a `data-testid` on every link, button, field, form and message (kebab-case), plus record ids on list rows. A test parses every page and fails if any element misses one.
- Security: login cookie HttpOnly + SameSite=Lax (+ Secure on https); a CSRF token on every form; "next" after login only goes to pages of this site; strict Content-Security-Policy, no framing; values escaped (a `<script>` review shows as text); card numbers and passwords never shown back.
- Beginner friendly and accessible: labels on every field, errors next to the field (`aria-describedby`), skip link, visible focus, 44 px touch targets, works at phone width, times in the reader's own time zone, confirm before cancel and reset. Plain CSS, no outside files (works offline).
- Found and fixed while checking screenshots: extra field settings (placeholder, maxlength) were escaped into the wrong text.
- Tests: 19 new web tests; all 128 app tests pass on SQLite and on the Docker databases; 148 tests in the repo.
- New packages, checked on PyPI and pinned with hashes: jinja2 (Pallets), python-multipart.
- DESIGN.md ("How the web pages work", test ID rules) and README updated.

**How to check**

`cd practice-app && ../.venv/bin/python -m bookshelf`, open http://127.0.0.1:8080, log in as `arshad` / `Test@1234`, add a book to the cart and pay with `4242 4242 4242 4242`. Log in as `admin` / `local_only_password` for the admin page.

**Next step**

Step 1.5.5: email through Mailpit (sign-up code, reset code, order confirmation), profile picture and product image upload, invoice PDF download.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.3: databases and Faker seed data

**Done**

- `practice-app/docker-compose.yml`: PostgreSQL 17.12 (main), MySQL 8.4.13 (reporting copy), MongoDB 8.0.38 (reviews). Images pinned to exact version and digest; ports on 127.0.0.1 only (55432, 53306, 57017); passwords from `.env` with fake defaults; health checks. Step 1.5.6 adds the app and Mailpit to it.
- The app chooses its databases from `.env`: no settings means SQLite files (no Docker needed); the three URLs mean PostgreSQL + MySQL + MongoDB. `/api/version` says which is in use; `/api/health` shows each one up or down.
- Reviews: one store with two backends (MongoDB collection with a unique index, or a SQL table). The API does not know which one it uses.
- Reporting copy (`order_facts`, `daily_sales`): refreshed every 60 seconds by a background thread and on demand with `POST /api/admin/reporting/sync`. Each sync rebuilds both tables in one transaction. Checked live: a new order reached MySQL within seconds, not at once (good material for "the copy lags" lessons).
- Faker seed: 40 customers (all `@example.com`, a few unverified) with about 65 orders in every status, coupons, payments and about 20 reviews. Fixed seed, so the same data on every computer. The fixed data lessons rely on did not change. A reset with all of it takes about 1.2 seconds.
- Bug found by running the tests on PostgreSQL: `POST /api/admin/reset` froze, because the request's own read of the users table held a lock that `DROP TABLE` waited for. Fixed by ending that transaction first. SQLite does not lock this way, so the SQLite tests could not catch it.
- Tests: 8 new (reporting, Faker data). All 109 app tests pass on SQLite and on the Docker databases (`BOOKSHELF_TEST_*` settings); 129 tests in the repo.
- New packages, checked on PyPI and pinned with hashes: psycopg (binary), pymysql, pymongo, faker.
- Mailpit's host port moves from 8025 to 58025 in DESIGN.md: 8025 is already used by another project on the owner's computer, and others may have the same clash.
- `.env.example`, README (start with Docker, how to connect to each database) and DESIGN.md updated.

**How to check**

`cd practice-app && docker compose up -d`, copy `.env.example` to `.env` and remove the `#` in front of the three `*_URL` lines, then `../.venv/bin/python -m bookshelf`. `/api/version` lists postgresql, mysql and mongodb. Connect a database client to the addresses in the README.

**Next step**

Step 1.5.4: the web pages (Jinja2), with a `data-testid` on every element.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.2: Practice App API

**Done**

- `practice-app/bookshelf/`: the Bookshelf API in FastAPI, 35 endpoints under `/api`. Covers sign up with a 6-digit email code (10 minutes, single use, burned after 5 wrong tries), resend code, login with a JWT bearer token (30 minutes), lockout after 5 wrong passwords (15 minutes), forgot and reset password, profile, products with search, category, price and stock filters, sorting and pages (at most 50), admin product changes (soft delete), reviews (buyers only, once), cart (1 to 10 per line, never above the stock), coupons (`WELCOME10` once per customer, `FREESHIP`, `SPRING25` already ended), checkout with the three sandbox cards, my orders, cancel (stock back, payment refunded), admin orders (paid to shipped to delivered), reset, a clock that admins can move, health and version.
- Built in for testers: one error shape everywhere (`{"error": {"code", "message", "request_id"}}`), an `X-Request-ID` header on every response, the `/docs` page with a "Try it" guide.
- Security: Argon2 password hashes; login tokens signed with `SECRET_KEY` and checked against the app clock; one-time codes stored as HMACs; the same answer for unknown users on login and forgot password (and the same check time); other customers' orders look "not found"; passwords never echoed in errors; binds to 127.0.0.1 by default.
- Runs without Docker for now: SQLite file in `practice-app/data/` (ignored by git); emails print in the terminal and are saved in `data/outbox/` until Mailpit (step 1.5.5). Fixed seed data (3 users, 3 categories, 13 products, 3 coupons, 2 delivered orders with reviews); Faker data comes in 1.5.3.
- `practice-app/tests/`: 101 tests for the app's own rules (121 tests in the repo now, about 2 seconds).
- New packages (owner approved), pinned with hashes in `practice-app/requirements.txt`: fastapi, uvicorn, sqlalchemy, pyjwt, argon2-cffi. Test client: `httpx2` in `requirements.txt` (the httpx successor that Starlette now asks for; same author, pydantic organisation) instead of `httpx`. The packages for later steps (database drivers, Jinja2, uploads, PDF, Faker) are added in those steps.
- `practice-app/.env.example` (fake values), `practice-app/README.md` (how to start it, logins, sandbox cards), DESIGN.md brought in line with what was built (resend code, remove coupon, read clock, OTP attempts, coupon code on carts and orders, refunded payments, reviews table in SQLite mode, the shipping and rounding rule spelled out). pytest and ruff settings and the setup command now include the app.
- Checked by running it: start, login, search, cart, checkout, error shape, `/docs` page and the emailed code in the terminal all work.

**How to check**

`cd practice-app && ../.venv/bin/python -m bookshelf`, then open http://127.0.0.1:8080/docs and log in as `arshad` / `Test@1234`. Or run `.venv/bin/pytest practice-app/tests`.

**Next step**

Step 1.5.3: PostgreSQL as the main database, the MySQL reporting copy (with the sync), MongoDB for reviews, and Faker seed data.

---

## 2026-11-15 · Phase 1.5 · Step 1.5.1: Practice App feature list and data model

**Done**

- `practice-app/DESIGN.md`: the plan for **Bookshelf**, the Practice App (a small book shop). Roles and seeded logins (Arshad, Maria, admin; clearly fake); v1.0 features written as user stories with acceptance criteria (sign up with email OTP, login lockout, profile picture upload, search and filters, reviews, cart limits, coupons, sandbox payment cards that succeed, fail or time out, orders, cancel, invoice PDF, admin, reporting sync, reset); built-in tester tools (API docs, `/status` health page, version, `data-testid` on every element, clock control for time lessons, request IDs).
- Architecture diagram and the full data model as a Mermaid ER diagram (13 tables), plus the MySQL reporting tables and the MongoDB review document. Money in cents, times in UTC.
- API endpoint list, web page list, safety rules, a planted-bug policy (no spoilers in code; answers in one file; `PRACTICE_APP_BUGS=off` shows correct behavior), and a version plan (1.1 to 1.5) for what later topics need: metrics and flaky endpoints, GraphQL, WebSocket and gRPC, message queue and a second service, AI helpers with a fake model.
- Choices inside the brief: FastAPI, PostgreSQL 17, MySQL 8.4, Mailpit, Docker Compose. Added from the decided multi-database set (MySQL, PostgreSQL, SQLite, MongoDB): MongoDB for reviews, and SQLite for a no-Docker mode so beginners can start before the Docker lesson. Host ports avoid common defaults (API 8080, PostgreSQL 55432, MySQL 53306, MongoDB 57017, Mailpit 8025); all bind to 127.0.0.1.
- `practice-app/README.md` placeholder. Both diagrams checked: they render with no errors.

**How to check**

Open `practice-app/DESIGN.md` on GitHub (diagrams render there).

**Next step**

Step 1.5.2: the API (auth, users, products, search, cart, checkout, orders, admin) with its own tests.

---

## 2026-11-15 · Phase 1 · Gate check (approved)

Gate: "the site runs locally, looks finished with placeholders, and a new topic can be added in under 10 minutes."

| Gate item | Result |
| --- | --- |
| Runs locally | Pass. `zensical serve` answers (HTTP 200); `zensical build --strict` has no warnings; `scripts/check.sh`: all 12 checks pass. |
| Looks finished with placeholders | Pass. All 78 built pages scanned: each has a title and a real description, none is empty, no visible TODO / template braces. Home and all 7 tabs reviewed in light and dark mode. Draft topics show "Coming soon" clearly. |
| New topic in under 10 minutes | Pass. Timed in a scratch copy (the real repo was not touched): one `new_topic.py` command plus two lines of text, then all 12 checks passed in **6 seconds** of machine time (about 2 to 3 minutes for a person). Menu, overview card, README map, Tags page and code folders updated by themselves. |

Phase 1 steps: 1.1 to 1.8 and 1.10 to 1.17 done. 1.9 (GitHub Discussions) moved to Phase 9 by decision, because Discussions and Giscus need the public repo. Optional owner inputs still open: About photo and a 2 to 3 line bio.

**Owner decision:** approved; move on and "complete the whole project first". The About photo and bio, GitHub Discussions (1.9) and the Code of Conduct contact are all handled in the last phase (Phase 9), not before.

---

## 2026-11-15 · Phase 1 · Step 1.17: share images, share buttons, credit line

**Done**

- **Share images:** `scripts/build_share_images.py` draws a 1200 x 630 PNG for every page (section, title, description for short titles, level, site name; site blue and the site's own font). Zensical 0.1.1 cannot make them yet. Owner approved adding **Pillow 13.0.0** (pinned with hashes in `requirements-docs.txt`). Images go into `site/` at build time and are cached in `.cache/share-images/` (git-ignored): nothing is committed, so the repo stays small at any size. 77 images in about 4 s; a rebuild uses the cache.
- **Share tags:** `overrides/main.html` adds Open Graph and X card tags (title, description, address, image, image size and alt) to every page.
- **Share buttons** (`overrides/partials/share.html`, `share.js`): LinkedIn, X, WhatsApp, "Copy link", and the phone share sheet where the browser has one. Plain links: nothing loads from those sites and nothing is sent unless the reader clicks. Hidden on drafts and with `hide: [share]`.
- **Share your progress:** section overviews show "You have finished X of Y topics", and when all are done a box with an editable message, Copy / LinkedIn / X / WhatsApp, and a gentle GitHub star request (no pop-ups). LinkedIn only takes the address, so clicking it also copies the message.
- **Credit line rule:** `scripts/check_credit_lines.py` checks that every file in a `templates/` folder starts with `Template from Zero to SDET: <site URL>`, in that file type's comment style (`#`, `//`, `--`, `<!-- -->`; after a `#!` or `<?xml` line if there is one; JSON and CSV skipped). `--fix` adds it. In `check.sh` and pre-commit; documented in the Style guide and `_new_topic_template/README.md`. 7 tests.
- `scripts/check_links.py` now also checks that every page's share image exists (caught all 158 when missing), and skips the per-page share addresses in `--external`.
- Fix found on the way: `docs/assets/images/IMAGES_NEEDED.md` (the owner's screenshot to-do list) was being published as a page. Now left out of the site with `exclude_docs`.
- About page privacy section mentions the share buttons.
- Checked in headless Chrome: share bar, partial progress (4 of 9, dark mode) and the "finished" box; external links: 209 addresses, none broken.

**How to check**

`scripts/check.sh` (12 checks, 20 tests). Share images: after `zensical build` and `scripts/build_share_images.py`, open `site/assets/images/social/`.

**Next step**

Phase 1 gate: the site runs locally and looks finished with placeholders, and a new topic can be added in under 10 minutes.

---

## 2026-11-15 · Owner request: new Pillar 6, AI-Powered QA (saved, built later)

**Done**

- `PROJECT_BRIEF.md` section 11: new "Pillar 6 — AI-Powered QA" with 11 topics (lessons and templates for each) and rules for the whole pillar: never send company code to unapproved AI tools; AI output is always reviewed by a person; template tests use a fake model so they run offline with no API key and no cost; keys only in `.env`.
- The old Pillar 3 topic "AI in testing" is merged into the new "Testing AI features" topic (no duplicate). Catalog is now 74 topics (70 learning + 4 Toolbox).
- Section 12: new **Phase 7.5** (after cloud and the capstone, before career). Its first step: choose the AI provider, add the section and its "Coming soon" pages, move the `advanced-testing/ai-in-testing` draft page into it (not published yet, so no redirect needed), add AI skills to the skills matrix and AI words to the Glossary.
- No site pages created yet, as the owner asked.

**Next step**

Unchanged: step 1.17.

---

## 2026-11-15 · Phase 1 · Step 1.16: readability check

**Done**

- The check itself was added to `scripts/check.sh` in step 1.12 (Flesch-Kincaid grade, prose only, target grade 8 or lower, drafts skipped). This step checked it against brief section 8A: grade 6 to 8, code skipped, too-hard pages listed. All requirements met.
- New: for a page that is too hard, the checker lists its longest sentences (over 25 words), so the writer knows what to split.
- New: `scripts/tests/test_check_readability.py`, 11 tests that prove the checker measures only what readers read (front matter, code, code in tabs, headings, tables, HTML, comments and link addresses are skipped; wrapped lines, list items and box titles are counted correctly) and that easy and hard text score as expected. `pyproject.toml` runs `scripts/tests` with the other tests.
- Tested on a deliberately hard page in a scratch copy: grade 38.1, the long sentences listed, `--strict` exits 1. In `check.sh` it stays advice only (warning), as the brief asks for a list, not a block.

**How to check**

`scripts/check.sh` (13 tests pass; every finished page is grade 6.0 or lower).

**Next step**

Step 1.17: share image for every page, share buttons, and the credit-line rule in `_new_topic_template/`.

---

## 2026-11-15 · Phase 1 · Step 1.15: progress tracker and the Skills Matrix

**Done**

- `docs/assets/javascripts/progress.js` (no libraries): progress saved **only in the reader's browser** (localStorage key `zts-progress-v1`). No account, nothing sent anywhere; works without JavaScript too (buttons stay hidden).
- **Lessons:** finished pages with a `level` get a "Mark this lesson as done" button at the end (`overrides/partials/content.html`), with a small check animation and a saved/blocked message. `hide: [progress]` turns it off for one page.
- **Across the site:** links to finished lessons get a ✓ in the menu and in lists; topic cards get a green "✓ Done" badge. On the lesson itself, only the menu entry gets the ✓ (not the headings or breadcrumb).
- **Learning Path:** "Your progress: X of Y lessons done" with a bar under each of the four paths (lists and the interview table).
- **Skills Matrix:** all 95 boxes can be ticked. A summary panel shows a bar per level, the total, "Your next skill" with its lesson link, and "Clear all ticks" (asks first). Each level heading gets its own bar.
- About page privacy section says where progress is saved. Style guide has a "Progress tracker" section.
- Tested in headless Chrome: ticks and "done" survive a reload in the same browser profile (3 of 95; Junior bar at 10%); marking API testing as done shows 1 of 11 and 1 of 12 on the two paths that include it, the menu ✓ and the card badge. Checked light, dark and narrow width; reduced motion turns off the animations.
- Deferred to step 1.17 (share buttons): the "Share your progress" message when a reader finishes a whole section.

**How to check**

Preview → Start Here → Skills Matrix: tick a few boxes, reload, they stay. Lesson buttons appear once real lessons are finished (all topics are drafts today).

**Next step**

Step 1.16: readability check (mostly done in 1.12), then 1.17: share images, share buttons and the credit-line rule.

---

## 2026-11-15 · Phase 1 · Step 1.14: Glossary, Tags and Start Here

**Done**

- **Tags:** `data/tags.yml` is the one list of allowed tags (42 subject tags, each with one plain sentence). Tags now say what a page is about (API, Database, Debugging), not which section it is in; every page was re-tagged (1 to 3 tags each).
- **Glossary:** `data/glossary.yml` holds 52 terms, each with a plain meaning and a link to the page that teaches it. The Glossary page is built from it: A to Z jump bar (stays at the top while scrolling), one anchor per term (`glossary.md#fixture`), and a highlight when you arrive from a link.
- **Hover explanations:** short forms (API, BDD, CI/CD, SQL, SDET...) show their meaning on hover on every page, from `includes/abbreviations.md` (generated, added to every page with `pymdownx.snippets.auto_append`). Headings stay clean (no dotted line).
- **Tags page:** a "jump to a tag" list of chips with page counts, above the full listing.
- **Start Here page:** what you need, four steps in order, "Already know some of this?" box, link to the Glossary.
- `scripts/build_reference.py` (with `--check`) builds the three files and checks: unknown tags, 0 or more than 3 tags on a menu page, duplicate terms, glossary links to pages that do not exist. Added to `scripts/check.sh` and pre-commit. Tested: each of those mistakes is caught.
- `scripts/new_topic.py` now needs `--tags` and rejects tags not in the list (tested). Templates, `CONTRIBUTING.md` and `STYLE_GUIDE.md` (new Tags and Glossary sections) updated.
- Checked in light, dark and narrow width. Note: headless Chrome cannot go narrower than 500 px, so narrow screenshots use 500 px.

**How to check**

`scripts/check.sh`. Preview: Toolbox → Glossary (click a letter; hover "API" in the tip box), Toolbox → Tags, and the Start Here tab.

**Next step**

Step 1.15: progress tracker (saved only in the reader's browser) and the skills matrix page.

---

## 2026-11-15 · Phase 1 · Step 1.13: README

**Done**

- `README.md`: banner, one-line promise, badges (website, MIT, CC BY 4.0, Python 3.13, pytest and Playwright, contributions welcome), quick links, "What is this?", a "lessons are being written" note, home page screenshot (light and dark), "I need to…" table, topic map, how to use it, what is in the repository, how to help, license, author.
- `.github/readme/`: `banner.svg` (hand-made, system fonts, no external requests) and `site-light.png` / `site-dark.png` (about 140 KB each, taken from the local build).
- The topic map is **generated** by `scripts/build_nav.py` from page front matter: one folded block per stage, topics in menu order and groups, summaries, and "coming soon" for drafts. The README stays short at any number of topics and never goes stale. The pre-commit menu hook now also watches `README.md`.
- `scripts/check_links.py` now checks README links too: website links must match a real page in `site/`, repository links a real file. Tested: a wrong page and a wrong file name are both caught.
- Badges are static shields.io images (GitHub proxies them, so readers are not tracked). The live star count badge waits for Phase 9, because a private repository shows an error badge.

**How to check**

`scripts/check.sh`. After the push, open the repository on GitHub to see the README; switch GitHub to dark mode to see the dark screenshot.

**Next step**

Step 1.14: Glossary, Tags and Start Here pages.

---

## 2026-11-15 · Phase 1 · Step 1.12: scripts/check.sh and ruff

**Done**

- `requirements.in` / `requirements.txt` (hashed): pytest 9.2.0, ruff 0.17.5, pyphen 0.18.1. Install: `uv pip sync --require-hashes requirements-docs.txt requirements.txt`.
- `pyproject.toml`: pytest (tests in `modules/` and the template) and ruff (style, bugs, naming, Bandit security rules; Markdown excluded so snippet lines are not broken).
- `scripts/check.sh`: one command, nine checks, summary at the end. Must pass: gitleaks (history, staged, unstaged), ruff check, ruff format, menu up to date, strict build, links, pytest. Advice only: hidden page dates, readability.
- `scripts/check_links.py` (standard library only): internal pages and #anchors always; `--external` visits every outside address. Own site URLs are checked against `site/`; LinkedIn counts as "could not verify"; own private repo skipped until Phase 9.
- `scripts/check_readability.py`: Flesch-Kincaid grade of each finished page's prose (code, tables, HTML, headings removed; wrapped lines joined). All 10 finished pages are grade 6.0 or lower.
- `scripts/update_page_dates.py --check`.
- Pre-commit: ruff check and ruff format hooks, using the hashed ruff in `.venv`.
- All existing Python cleaned to pass ruff (research script: https-only URL check, context manager, clearer names).
- Tested: two planted broken links caught; failing test makes `check.sh` exit 1 with a FAILED summary; external run: 159 links fine, LinkedIn unverifiable.

**How to check**

`scripts/check.sh` (about 2 seconds), or `scripts/check.sh --external`.

**Next step**

Step 1.13: README.

---

## 2026-11-15 · Phase 1 · Step 1.11: new topic template

**Done**

- `scripts/new_topic.py`: one command adds a topic: "Coming soon" page (draft), `modules/` folders (templates, examples, exercises, solutions, tests), then runs `build_nav.py`. Picks the order (last, or between two topics with `--after`), checks section, group and folder name, never overwrites.
- `_new_topic_template/` (not published): README with both stages, the full "First time? Start here" playbook page (brief 7.1), a lesson page skeleton (7.2: before you start, code tabs pulled from `modules/` with snippets, common mistakes, error box, exercise, quick check, references), an example template with the credit line, and its test.
- Tested in a scratch copy: grouped and ungrouped sections, `--after` gives order 25 between 20 and 30, six error cases stop with a clear message, strict build passes. Template tests pass.
- CONTRIBUTING: the quick way first.
- Owner decision: Code of Conduct contact is discussed again in Phase 9 (saved in memory).

**Next step**

Step 1.12: `scripts/check.sh` (build, menu check, tests, link check, gitleaks, readability) and ruff in pre-commit.

---

## 2026-11-15 · Phase 1 · Step 1.10: repository documents

**Done**

- `LICENSE` (MIT, standard text so GitHub detects it) and `LICENSE-CC-BY-4.0.txt` (official legal code from creativecommons.org, with a header saying which files each license covers). Fonts keep their OFL.
- `CODE_OF_CONDUCT.md`: Contributor Covenant 2.1 (official text), contact = private LinkedIn message, scope names issues, PRs, Discussions and lesson comments.
- `SECURITY.md`: brief section 9, plus private reporting through GitHub, and a note that the Practice App's planted bugs are not vulnerabilities (localhost only, never deploy it).
- `STYLE_GUIDE.md`: brief sections 7 and 8 copied by script, plus site conventions (front matter fields, boxes, no visible dates).
- `CONTRIBUTING.md`: setup with uv and hashed installs, how to add a topic (front matter + `build_nav.py`), the lesson checklist (brief section 13), licenses.
- `.github/ISSUE_TEMPLATE/`: "Content error" and "Template or code problem" forms (privacy reminders), blank issues off, security link. `.github/PULL_REQUEST_TEMPLATE.md` with the checklist.
- 👎 feedback link now opens the "Content error" form with the page address filled in.
- Brief updated: navigation order lives in front matter; author line has no visible date.

**Open questions**

- Code of Conduct contact: LinkedIn message for now. **Owner decision: discuss again in Phase 9** (CI/CD time); the owner may create a project-only email then, with GitHub "Report content" as backup.
- The GitHub CLI on this machine is logged in to a different account, so labels `content` and `code` were not created. Create them when convenient (or in Phase 9).
- Phase 9: turn on private vulnerability reporting (Settings, Security) when the repo is public; add Discussions links to `config.yml`.

**Next step**

Step 1.11: `_new_topic_template/` (a ready topic folder to copy, with the front matter fields).

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

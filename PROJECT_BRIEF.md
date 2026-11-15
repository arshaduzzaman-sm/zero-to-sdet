# Zero to SDET — Project Brief for the AI Assistant

> Read this whole file before doing anything. It is the single source of truth for this project.
> If something here conflicts with what you see in the repository, follow this file and tell me about the conflict.
> If something is unclear or missing, ask me. Never guess.

---

## 0. How to work with me

1. **Read this file fully.** Then inspect my repository: every folder, every file, and the git history.
2. **Report back before changing anything.** Give me:
   - a list of every existing file, with a suggestion for each: keep, move (to where), rewrite, or delete, and why;
   - any secrets, passwords, personal paths, usernames or emails you found in files **or in git history**;
   - any conflict between this brief and the current repo.
3. **Wait for my approval** before moving, rewriting or deleting anything. Never delete without my explicit "yes".
4. **Work one phase at a time, one step at a time** (see section 12). After each step, stop and show me:
   - what you changed (files created, moved, edited);
   - how I can check it on my computer (exact commands and what I should see);
   - what the next step is.
5. **Do not set up any CI/CD (GitHub Actions workflows) until Phase 9.** During building, everything runs locally.
6. **Never commit or push for me** unless I ask. When I ask, run the pre-push security checklist (section 9) first.
7. Fill in any remaining placeholders only with values I give you. If a value is missing, ask.
8. **Keep `PROGRESS.md` up to date.** This project runs over many sessions. After every finished step, add an entry: date, phase and step, what was done, files changed, open questions, and the next step. Read it at the start of every session (`CLAUDE.md` says so too). Never put secrets or personal data in it.

---

## 1. Project summary

Turn my GitHub repository, currently called **"Python SDET"** (a folder of messy practice files), into **Zero to SDET**:

1. a **well-organized repository** of real, reusable test templates and lessons, and
2. a **free, public learning website** built from that repository and hosted on GitHub Pages.

The goal: a person with no automation experience can follow the website and become a **professional SDET**, all the way to **senior level**. Nothing on the site should be impossible to understand for a beginner.

All content is in **simple, clear English**.

### Name and identity (decided)

| Item | Value |
| --- | --- |
| Project name | **Zero to SDET** |
| Repository name | `zero-to-sdet`: a **new** repository created fresh in Phase 0 (see section 3A) |
| Site title | **Zero to SDET — Everything you need to become a professional SDET** |
| Tagline | *Learn software testing and test automation, step by step. Real templates and code you can use at work. Free.* (changed 2026-11-16: no level words) |
| GitHub topics | `sdet`, `sdet-roadmap`, `qa-to-sdet`, `test-automation`, `python`, `pytest`, `api-testing`, `bdd`, `qa` |

Use the name and tagline consistently in `zensical.toml`, the README, the home page, the social preview image and the About page.

I am the **only author**. My name appears on the site (see section 10).

---

## 2. Who it is for, and the two core ideas

### Readers

| Reader | What they need |
| --- | --- |
| Someone who has never tested | Simple words, every step shown, what to do when stuck |
| Manual tester moving to automation | A clear path, templates to copy |
| Engineer who already automates | Real-world patterns, frameworks, debugging, team workflow, advanced topics |
| Engineer who leads quality | Test architecture, quality strategy, mentoring, leading quality |
| Job seeker | Interview prep, portfolio project, career roadmap |
| Anyone at work with a task today | The one page that solves their problem right now |

**For everyone (owner decision, 2026-11-16).** The site never sorts readers into levels. Phrases like "zero to mid level", "junior to mid-level" or "first test to senior level" are not used anywhere: in taglines, the home page, the Learning Path or the Skills Matrix (which is grouped by skill area, not by level). Each page must answer the question of someone who has never tested, of an engineer stuck on a task today, and of an experienced engineer looking for a template.

**Real templates (owner decision, 2026-11-16).** Templates are the scripts, code snippets, checklists and plans people really use at work, ready to copy and adapt. No toy exercises. Every topic also covers what to do when stuck, how to plan, and what to do at each stage.

**The author's note (owner decision, 2026-11-16).** Home (short) and About (full) carry the author's note: the content comes from the author's own work and from what many people have shared online; the author gathered it in one place, in plain words, and thanks them.

### Core idea 1: learn it on the job

The typical reader is someone whose company just said "test the database" or "set up BDD", and who has never done it. Every topic teaches them **how to think about the task, how to plan it, and how to learn the rest on their own**, not only which commands to type. Every fact links to the original source so they can go deeper.

### Core idea 2: every page stands on its own

The site has a recommended order (junior → senior), but **many readers will jump straight to the page they need**. So:

- Every page starts with a **"Before you start"** box: prerequisites as links, plus a 2–3 sentence recap of any concept the page depends on. A reader who lands here from Google can still follow it.
- Never write "as we saw earlier" or "remember from the last lesson" without a link to that page.
- Every term is linked to the Glossary the first time it appears **on each page**.
- Every topic's index page has a **"Jump to what you need"** list of quick links.
- The home page has an **"I need to…" task finder** (see section 4).
- Breadcrumbs, search, level badges and tags on every page, so readers always know where they are.

### Core idea 3: nothing is missing

The site must cover **every** skill a professional SDET needs, from first test to senior level, with no gaps. This is checked, not hoped for:

- **Skills matrix.** In Phase 0, build `docs/start-here/skills-matrix.md`: one table of every SDET skill, grouped by level (Junior / Mid / Senior / Lead), each linked to the lesson that teaches it. Build it from three sources:
  1. the topic catalog in section 11;
  2. at least 30 real, current SDET and QA automation job ads (junior to senior, several countries). List every skill they ask for, and count how often each appears;
  3. public testing syllabi and standards, for example the ISTQB Foundation and Test Automation Engineering syllabi and the ISTQB glossary.
- Any skill found in sources 2 or 3 that has no lesson is a **gap**. Report gaps to me and add them to the catalog.
- The skills matrix is also a page for readers: a checklist they can tick to see where they stand and what to learn next.
- The coverage check is repeated at the end of every phase and in Phase 9.
- **Equal depth (decided 2026-11-15).** There is no "main" topic and no "side" topic. Every topic, and every tool inside a topic (for example both behave and pytest-bdd), gets the full playbook, full lessons, complete templates with tests, and a Bug Hunt. A reader who learns only from this repository must be able to grow to senior and lead SDET level without needing another course.

---

## 3. Non-negotiable rules (summary)

1. **Security first.** Nothing that exposes my computer, accounts, employer or personal data is ever published. Full rules in section 9.
2. **Human teacher voice.** Write like an experienced human teacher, never like an AI. Full rules in section 8.
3. **Everything runs.** Every code sample works on the first try, and has a test.
4. **Official sources.** Every page links to the original documentation it relies on.
5. **No CI/CD until Phase 9.** Local preview and local tests only until then.
6. **Ask, don't guess.** Ask me whenever something is unclear.
7. **No deletions without approval.**

---

## 3A. Repositories, hosting and domain (security plan)

### Repositories

| Repository | Visibility | Purpose |
| --- | --- | --- |
| `python-sdet-practice-archive` (the old "Python SDET" repo, renamed) | **Private forever** | My old practice files. Its git history contains a real password, so it is never made public. Nothing is deleted from it. |
| `zero-to-sdet` | **Private** during Phases 0–8, **public** from Phase 9 | The real project: lessons, templates, Practice App, website source. Created fresh, so its history starts clean. |
| My private notes | Private, outside `zero-to-sdet` | Personal notes, drafts with private details, screenshot originals before blurring. Never inside the public repo. |

Do **not** split the project into a private source repo plus a separate public "site only" repo:

- GitHub Pages on the free plan only works from a **public** repository. Private-repo Pages needs a paid plan, and the site is still public anyway.
- Giscus comments need a **public** repository with Discussions turned on.
- Stars, forks, "Edit this page" links, issues and contributors all live on the source repository. A hidden source repo loses the things that make the project grow.
- The templates and code are a big part of the value. Learners need to read and copy them.
- Two repositories means keeping them in sync by hand, which leads to mistakes.

### The four stages

1. **Build in private (Phases 0–8).** `zero-to-sdet` is private. The site is previewed locally with `zensical serve`. gitleaks runs on every commit.
2. **Audit, then go public (Phase 9).** Run the full security audit (section 9) and a full-history gitleaks scan. If anything was ever committed that should not be public, publish a fresh, squashed history instead of the current one. Then switch the repo to public, turn on Discussions, Giscus and GitHub Pages.
3. **Work in public (after launch).** New work goes on branches (for example `draft/contract-testing`) and is merged only when it meets the definition of done. Unfinished pages are marked as drafts and left out of the build. Personal notes stay outside the repo.
4. **Custom domain (any time later).**
   - Buy the domain from a registrar that supports 2FA and domain lock. Turn both on.
   - Verify the domain in GitHub account settings before pointing it at Pages. This stops anyone else from taking it over.
   - Add the custom domain in the Pages settings and enforce HTTPS.
   - Keep the site URL in one place (`zensical.toml`), so changing it is one edit, and add redirects so old links keep working.
   - The site is plain Markdown, so it can move to another host later (for example Cloudflare Pages or Netlify) without rewriting anything.

### Account security

- Two-factor authentication on GitHub (an authenticator app or passkey, not SMS), on LinkedIn, and on the domain registrar.
- Use GitHub's no-reply email for commits, and hide my email in GitHub settings.
- Use SSH keys with a passphrase, or fine-grained access tokens with an expiry date and the smallest permissions. Never store tokens in the repo.
- Review the apps and tokens that have access to my GitHub account every few months, and remove what is not used.

---

## 4. The website

### Technology

- Build the site with **Zensical** (the successor to Material for MkDocs, from the same team; it reads Markdown and is compatible with MkDocs-style configuration). Check the current Zensical documentation before configuring it, and tell me if a feature below is not supported yet and what you suggest instead.
- During building: preview locally with `zensical serve`.
- In Phase 9 only: deploy to GitHub Pages with a GitHub Actions workflow.

### Design

Simple, clean and calm. Learning comes first; decoration comes last.

- Light and dark mode, one main color (see open decisions), clean readable font.
- Top navigation tabs: **Home · Start Here · Think Like a Tester · Core Automation · Advanced Testing · Infrastructure · The Professional SDET · Toolbox · About**.
- Left sidebar for pages inside the current tab; right sidebar for "On this page" headings.
- Built-in search with suggestions.
- Copy button on every code block, code tabs, admonition boxes (tip, warning, common mistake, troubleshooting), collapsible blocks, Mermaid diagrams, task lists.
- Breadcrumbs at the top of every page.
- Level badge on every lesson: **Beginner / Intermediate / Advanced / Senior**.
- Tags on every page (for example `api`, `database`, `bdd`, `debugging`), with a Tags index page.
- Previous / next buttons at the bottom of every lesson.
- Works well on phones.

### Key pages

- **Home**
  - Hero: one-line promise, short intro, "Start learning" and "Star on GitHub" buttons.
  - **"I need to…" task finder:** cards such as "Test an API", "Check data in a database", "Test several databases", "Set up BDD", "Automate a web page", "Run tests in Docker", "Find out why a test is flaky", "Write a bug report", "Plan testing for a new feature", "Prepare for an SDET interview". Each card links straight to the right page.
  - **Learning paths by role:** Manual tester → automation; Junior → mid; Mid → senior; Interview prep in 4 weeks.
  - Cards for the five pillars and the Toolbox.
- **Start Here:** how to use the site, environment setup (Python, VS Code, virtual environment, Docker, with links out for absolute beginners), the Practice App tour.
- **Learning Path:** a Mermaid diagram of the full junior → senior journey.
- **Glossary**, **Tags**, **Changelog**, **About**.

### Search engine rules (SEO)

Most visitors will arrive from Google on a single lesson page, so every page is written to be found.

- **Page titles match what people type into search.** Good: "How to Test a REST API with Python (Step by Step)", "Database Testing for Beginners: A Practical Guide", "Manual Tester to SDET: Where to Start". Bad: "Lesson 3", "API Part 2".
- Every page has a meta **description** of 1–2 sentences (under about 155 characters) saying what the reader will be able to do.
- One clear `#` heading per page; `##` and `###` headings use the words people search for.
- Short, readable URLs taken from the page title, for example `/core-automation/api-testing/get-requests/`. Never change a published URL; add a redirect if a page moves.
- Descriptive alt text on every image; descriptive link text (never "click here").
- Internal links between related pages, so readers and search engines can move through the site.
- Generate a sitemap, and add the site to Google Search Console in Phase 9.
- The social preview image and page titles also make shared links look good on LinkedIn, X and WhatsApp.

---

## 5. Repository structure

```text
zero-to-sdet/
├── README.md                  # repo intro, badges, website link, topic map
├── PROJECT_BRIEF.md           # this file
├── CLAUDE.md                  # short session-start instructions for Claude Code
├── PROGRESS.md                # log of finished steps and the next step
├── zensical.toml              # site name, colors, author; navigation generated by scripts/build_nav.py
├── STYLE_GUIDE.md             # writing voice and page rules (sections 7 and 8)
├── CONTRIBUTING.md            # checklist for adding a new topic
├── SECURITY.md                # security rules and how to report a problem
├── CODE_OF_CONDUCT.md
├── LICENSE                    # MIT for code, CC BY 4.0 for text
├── CHANGELOG.md
├── requirements.txt           # code dependencies (pinned)
├── requirements-docs.txt      # website dependencies (pinned)
├── .gitignore
├── .env.example               # fake example values only
├── .pre-commit-config.yaml    # gitleaks and ruff, run locally
├── scripts/
│   └── check.sh               # runs all tests, link check and gitleaks locally
├── docs/                      # website pages
│   ├── index.md
│   ├── start-here/
│   ├── learning-path.md
│   ├── about.md
│   ├── glossary.md
│   ├── tags.md
│   ├── think-like-a-tester/
│   ├── core-automation/
│   │   ├── api-testing/
│   │   │   ├── index.md       # "First time? Start here" playbook
│   │   │   ├── http-basics.md # one concept per page
│   │   │   └── get-requests.md
│   │   └── ...
│   ├── advanced-testing/
│   ├── infrastructure/
│   ├── professional-sdet/
│   ├── toolbox/
│   └── assets/
│       ├── images/            # docs/assets/images/<topic>/<page>-<n>.png
│       └── diagrams/
├── modules/                   # runnable code; mirrors docs/
│   └── core_automation/
│       └── api_testing/
│           ├── templates/
│           ├── examples/
│           ├── exercises/
│           ├── solutions/
│           └── tests/
├── practice-app/              # the demo shop every lesson tests (section 6)
├── _new_topic_template/       # copy this to start a new topic
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/             # added only in Phase 9
```

### Rules that keep it scalable

1. **No numbers in folder names.** The order lives in each page's front matter (`order:`), and `scripts/build_nav.py` builds the navigation in `zensical.toml` from it (decided 2026-11-15), so a new topic can go anywhere without renaming.
2. `docs/` and `modules/` mirror each other: every topic has the same path in both.
3. Code shown on the site is **pulled from the real files in `modules/`** with snippet includes, never copy-pasted.
4. One concept per page. A topic is a folder of short pages.
5. Every new topic starts from `_new_topic_template/` and follows `CONTRIBUTING.md`.
6. Every template has a test. Run them all locally with `scripts/check.sh` before each push. After Phase 9, CI runs them too.
7. Published URLs never change. If a page moves, add a redirect.

---

## 6. The Practice App

A small online shop built for testing, in `practice-app/`. **Every topic tests this same app**, so lessons connect: the API lesson creates an order, the database lesson checks it was saved, the BDD lesson describes checkout in Gherkin, the performance lesson puts it under load.

- **Features:** sign up and log in (token auth), users, products, search, cart, checkout, orders, an admin role, email and OTP messages, file upload and download.
- **Parts:** REST API (FastAPI) with auto-generated API docs, a simple web page, PostgreSQL as the main database, MySQL as a reporting copy (for multi-database lessons), Mailpit to catch emails, and later a message queue.
- **Start:** `docker compose up`. A reset script restores the original data. A health check page shows everything is running.
- **Running it online:** GitHub Codespaces only (owner decision, 2026-11-15). A "Open in Codespaces" button gives each learner their own private copy of the whole app in the cloud, with nothing to install. The app is never hosted on a shared public server, and GitHub Pages hosts only the lesson site (it cannot run the app).
- **Data:** fake only, seeded with Faker. Passwords are clearly fake (for example `local_only_password`), loaded from `.env`. Every service binds to `localhost` only.
- **Planted bugs:** about 30 deliberate bugs across API, database, UI, security and performance, added over time: a starter set in Phase 1.5, the rest when the topic that needs them is written. Each topic ends with a **"Bug Hunt"**: the reader finds the bugs and writes bug reports. Answers sit on a separate solutions page, folded by default.
- **The pages are the product (owner decisions, 2026-11-15 and 2026-11-16).** Running the app means downloading the repository and starting it locally, so most readers never will. Lessons use real job situations as examples and show every output on the page. The app appears only in an optional "Try it on the Practice App" box.
- **Earlier wording (2026-11-15):** The site is the main product; the app is a helper. After Phase 1.5 the app only changes when a lesson needs it. Many readers will never run the app, so every lesson must teach fully from the page alone (section 7.3).
- **Versioned:** each lesson names the app version it uses, so updates never break old pages.

---

## 7. Content standards

### 7.1 Topic playbook: "First time? Start here"

Every topic's `index.md` is a playbook for someone doing this for the first time at work. It walks through one realistic request (for example, "Your manager says: we're adding BDD, can you set it up?") from start to finish, in these steps:

1. **Understand the ask.** Questions to ask your lead on day one: what system, why now, what "done" means, deadline, environments, access.
2. **Picture the system.** A simple diagram of what you are testing and where the data flows.
3. **Learn just enough.** A 30–60 minute reading path through the official docs, in order, with what to skip for now.
4. **Get something running.** Copy the topic's template and get a first result in the reader's own project within an hour (the Practice App is an optional place to try it).
5. **Decide what to test.** Test ideas specific to this area, sorted by risk, using the test design techniques.
6. **Write a one-page plan** with the test plan template, and share it before building.
7. **Build in small steps.** Smoke test, then happy path, then negative cases, then edge cases.
8. **Report and get feedback.** What to show your team, and how.
9. **Keep learning on your own.** What to read next, practice ideas, and official docs to bookmark.

Each playbook also has a **"How an experienced SDET thinks about this"** box, a **"Red flags"** box (signs the plan is going wrong), a **"Jump to what you need"** link list, and an **"Official resources"** list at the end.

### 7.2 Lesson page template (top to bottom)

1. Title and a one-sentence summary.
2. Info bar: level, reading time, tags.
3. **"Before you start"** box: prerequisites as links, plus a short recap so the page stands on its own.
4. **"What you will learn":** three to five outcomes.
5. **"Why this matters at work":** a real situation.
6. The concept in plain words, starting with an everyday comparison and a diagram.
7. Step-by-step walkthrough: exactly what to type, and a screenshot or expected output after each step.
8. The template: code tabs (code · how to run · expected output), pulled from `modules/`.
9. **"Common mistakes"** box.
10. **"If you see this error"** box: the real error text and the fix.
11. **"Try it yourself":** an exercise from a real job situation, with the solution (and its result) in a collapsed block.
12. **Quick check:** three questions.
13. **References:** every source used, plus the tool version the page was written for and the date the links were last checked.
14. Footer: previous / next, "Edit this page on GitHub", comments, feedback widget, author line.

### 7.3 Teaching method

- Start with a picture or everyday comparison, then the real thing. Example: "An API is like a waiter who takes your order to the kitchen and brings back your food."
- Show, then do: a diagram of the idea, then a guided walkthrough, then the reader does it alone.
- One new idea at a time. If a page needs three new ideas, it becomes three pages.
- After every few steps, a **"Check: you should now see…"** line with a screenshot.
- When something can go wrong, show the real error and the fix.
- **Learn from the page alone (owner decision, 2026-11-15).** A reader who never installs or runs anything must still learn everything: every command, request and click is followed by its real output or a screenshot on the page, and every exercise solution shows the result too. Running the Practice App is an optional way to practise, never a requirement to understand.

### 7.4 Install and setup steps (every tool)

- Tabs for **macOS, Windows and Linux**.
- The exact version used, with a link to the **official** download page only.
- The command to type, then a **verify command** with its expected output (for example `python3 --version` → `Python 3.12.x`).
- A screenshot of every installer screen and settings window, with the right button highlighted.
- A **Troubleshooting** box for the most common problems.
- A folder tree showing where each file goes, before the reader creates it.
- How to uninstall or clean up.

### 7.5 Visuals checklist (every page)

- At least one **Mermaid diagram** for any flow, architecture or sequence.
- A **screenshot** for every step in a UI (VS Code, browser DevTools, database tools, GitHub), with arrows or highlights.
- A **terminal output** block for every command.
- **Alt text** on every image.
- Images at `docs/assets/images/<topic>/<page>-<n>.png`, compressed under 300 KB.
- Where a screenshot is still needed, add a placeholder image link and list it in `docs/assets/images/IMAGES_NEEDED.md` with a description of exactly what to capture. I will take the screenshots myself.
- One illustrated **cheat sheet image** per topic that people can save and share.

### 7.6 References and sources

- Official sources first: the tool's own documentation (for example docs.pytest.org, the Requests docs, the MySQL and PostgreSQL manuals, the Cucumber Gherkin reference), standards bodies (W3C for accessibility, OWASP for security, the ISTQB glossary for testing terms), and original authors' articles.
- Link inline, right where a fact or rule is used.
- End every page with a **References** list.
- Run a link check locally before each push (in `scripts/check.sh`). From Phase 9, also weekly in CI.
- Never link to pirated books, copied content or low-quality sites.

### 7.7 Code rules

- Every example runs and has a test.
- No passwords or keys in code: use `.env` plus `.env.example`.
- Pin library versions.
- Format and lint with `ruff`. Use type hints and short comments that explain **why**, not what.
- Use Python 3.12+ and pytest as the base for all templates. Exceptions, where the tool has its own runner: behave (BDD), Robot Framework, Locust, k6 and JMeter. Their templates still have a check that `scripts/check.sh` runs.
- Every template file starts with one credit comment line: `# Template from Zero to SDET: <site URL>`.

### 7.8 Example names and data

- The main example person in the site is **Arshad** (first name only). Use him wherever an example needs a person:
  - Practice App main test user: username `arshad`, name `Arshad`, email `arshad@example.com`, password `Test@1234` (clearly fake).
  - Code: `create_user(name="Arshad")`, `assert response.json()["name"] == "Arshad"`.
  - Gherkin: `Given Arshad is logged in`, `When Arshad adds 2 books to the cart`.
  - SQL: `INSERT INTO customers (name) VALUES ('Arshad');`
  - Stories: "Arshad just joined a new team. On his first day, his lead asks him to test the checkout API…" (clearly an example, never presented as real experience).
- **Never** use a full name, a real email, phone number, birth date, address or any password pattern I really use. Emails always end in `@example.com`.
- Arshad is not the only person: second users, admins and customer lists use other names (Faker or common names from many countries), for example "Arshad must not be able to see Maria's order".

---

## 8. Writing style (also save as `STYLE_GUIDE.md`)

Write like an experienced human teacher sitting next to one learner.

- Use "you" and "we", in plain English that a 10-year-old could follow.
- Explain **why** before **how**.
- Define every new word the first time it appears on a page, and add it to the Glossary.
- Use real work situations. Example: "Your team moved customer data from MySQL to PostgreSQL. How do you prove nothing was lost?"
- **Never invent personal stories, fake experience, fake statistics or fake quotes.**
- Mix short and long sentences. Be warm, direct, and honest about what is hard.
- Keep paragraphs short. Use lists only for real lists or steps.
- Every command shows what you type **and** what you should see.
- **Banned phrases:** "In today's fast-paced world", "Let's dive in", "dive deep", "It's not X, it's Y", "Moreover", "Furthermore", "In conclusion", "Unlock", "Seamless", "Robust", "Leverage", "Game-changer", "Delve". No emoji spam.
- Read each page aloud once. If it sounds like a robot or a sales page, rewrite it.

### 8A. The 10-year-old test

Every explanation must make sense to a curious 10-year-old reading it with no help. Technical words are allowed, but only after they are explained.

- Each concept page opens with an **"In plain words"** box: two or three sentences and an everyday comparison, before any technical detail. Example: "A database is like a giant, super-organized notebook. Each table is one page, and each row is one line on that page."
- Every concept gets a **picture**: a diagram, an illustration or an annotated screenshot.
- Sentences stay short (aim for under 20 words). One idea per paragraph.
- No unexplained abbreviations. Write "API (Application Programming Interface): a way for two programs to talk" the first time on every page.
- Explanations aim for a reading level around school grade 6–8. `scripts/check.sh` runs a readability check (for example with the `textstat` library) on the prose of each page, skipping code blocks, and lists pages that score too hard.
- Before a page is done, read it as if you had never heard of the topic. Anything you would have to look up is explained on the page or linked.

---

## 9. Security and privacy rules (also save as `SECURITY.md`)

The repository and website are **public**. Nothing may be published that exposes my computer, accounts, employer or personal data. Check every file, screenshot and commit against these rules.

### Never publish

| What | Examples | Do this instead |
| --- | --- | --- |
| Passwords, API keys, tokens | Database passwords, GitHub tokens, cloud keys | `.env` (git-ignored) + `.env.example` with fake values |
| Personal details | My email, phone, address | GitHub's no-reply commit email; contact only via About page links |
| Computer details | Username and machine name in the terminal prompt, `/Users/<name>/...` paths, local IPs, Wi-Fi names | A neutral prompt (for example `$`) and generic paths like `~/projects/zero-to-sdet` |
| Employer or client material | Company code, URLs, data, screenshots, ticket text | The Practice App and public practice APIs |
| Real people's data | Names, emails, any production data | Fake data from Faker |
| Hidden image data | GPS and device info in photos | Strip metadata before adding images |

### Screenshot rules

- Clean setup: neutral terminal prompt, no personal bookmarks, no notifications, no other tabs or apps.
- Blur or crop any username, email, path, token, IP address or account name.
- Show only `localhost`, `example.com` and public practice sites.
- Remove image metadata before committing.

### Code and repo rules

- `.gitignore` covers `.env`, `.venv/`, `__pycache__/`, `.DS_Store`, IDE folders, logs, reports, database files, and build output.
- Docker Compose uses clearly fake local passwords loaded from `.env`; services bind to `localhost` only.
- **gitleaks runs locally before every commit** through pre-commit.
- **Before the first public push, scan the full git history.** A secret that was ever committed stays in history even after deletion. If one is found: tell me, help me remove it with a history rewrite, and remind me to change that password.
- The MySQL password used in my old practice files has appeared in code and **must be changed**.
- Install libraries only from official sources, pin versions, and tell me before adding a new dependency.
- Giscus and any other integration get the smallest permissions they need.

### Pre-push checklist (run every time I ask you to commit or push)

- [ ] gitleaks passes; no secrets in the diff
- [ ] No personal paths, usernames or emails in text, code or screenshots
- [ ] New images cropped, blurred where needed, metadata removed
- [ ] `.env` not staged; `.env.example` holds only fake values
- [ ] No employer or client material

---

## 10. Author, community and growth

### Author branding

- Author: **Arshaduzzaman SM** (exactly as on my LinkedIn and GitHub; use this same form everywhere). GitHub: **arshaduzzaman-sm** (https://github.com/arshaduzzaman-sm). LinkedIn: https://www.linkedin.com/in/arshaduzzaman-sm/
- Name in the site header area, on every page footer ("© 2026 Arshaduzzaman SM"), on the About page, and in `LICENSE`.
- "Written by Arshaduzzaman SM" line on every lesson. No visible "last updated" date (decided 2026-11-15: an old date makes a correct lesson look abandoned); lessons show the tool versions they were tested with instead.
- About page: photo (I will provide it), short bio, why the site exists, links.
- License: MIT for code, CC BY 4.0 for text, so reuse requires credit.

### Ways visitors engage

| Feature | Where | How |
| --- | --- | --- |
| Star the repo | Home, README, footer | "Star on GitHub" button with live count |
| Comments | Bottom of every page | Giscus (stored in GitHub Discussions) |
| "Was this page helpful?" | Bottom of every page | Thumbs up / down, with a link to leave details |
| Ask a question | GitHub Discussions "Q&A" | Linked from every page |
| Suggest a topic | GitHub Discussions "Ideas" | Upvotes decide the roadmap |
| Report a mistake | Issue template "Content error" | Pre-filled with the page URL |
| Contribute | `CONTRIBUTING.md` + "Edit this page" | Good-first-issue labels |
| Follow updates | Changelog + GitHub Releases | One release note per new topic |

### What makes it shareable

- README that sells it in five seconds: banner image, one-line promise, badges, a screenshot of the site, the full topic map, the "I need to…" list.
- Custom social preview image.
- Per-topic cheat sheet images.
- Star History chart and contributors wall in the README (once there is traction).
- Search-friendly page titles and descriptions.
- Launch plan (Phase 9): LinkedIn, Reddit (r/QualityAssurance, r/softwaretesting), dev.to, Hacker News "Show HN", curated awesome lists.

### Growth plan: how this becomes the go-to SDET resource

Nothing guarantees going viral, but these features give the project the best chance. Build them in as listed in the roadmap.

**Features people share**

People share things that make them look good or genuinely help someone else. Never ship pre-written "post this" messages or pop-ups asking for shares.

- **SDET Skills Assessment:** a free quiz of 20–30 questions across all pillars. It ends with a clean result card, for example "Mid-level SDET: strong in API testing, grow in performance", with links to the lessons that close each gap, and a download-image and share button. It runs entirely in the browser; no answers or results are sent or stored anywhere.
- **Capstone as a portfolio:** learners publish their capstone project on their own GitHub and resume. The capstone README template includes a small "Built with Zero to SDET" badge linking to the site.
- **Credit line in every template:** each template file starts with one comment line, for example `# Template from Zero to SDET: <site URL>`. When people copy templates into work projects, teammates find the source. The CC BY / MIT licenses already require credit.
- **Share image for every page:** each page gets an automatic social preview image with its title, so shared links look good on LinkedIn, X and WhatsApp. Plus simple share buttons (LinkedIn, X, WhatsApp, copy link) at the bottom of each page.
- **Progress tracker:** readers tick lessons as done; progress is saved only in their own browser and shown on the Learning Path and skills matrix pages. When someone completes a pillar, show a small "Share your progress" option with a short, editable message.
- **Skills matrix checklist** (Junior → Lead) that people screenshot and share.
- **Cheat sheet images** for every topic, sized for LinkedIn and Instagram, with the site name and URL on each.
- **Interview question bank** with clear answers, plus "Add a question you were asked" so the community grows it (through a GitHub issue form, reviewed before it goes live).
- **Bug Hunts and a Hall of Fame:** readers who find all planted bugs in the Practice App post in Discussions and get listed in the README Hall of Fame (by GitHub username only, if they agree).
- A short **demo GIF** at the top of the README showing the site and the Practice App.
- After launch, if readers want it: **"Teach your team" slides** (5–8 slides per topic) for presenting a topic at work.

**Launch and after**

- Launch in Phase 9 on a Tuesday to Thursday: LinkedIn post with a carousel, Reddit (r/QualityAssurance, r/softwaretesting, r/learnpython), dev.to article, Hacker News "Show HN", Product Hunt, and pull requests to relevant awesome lists.
- After launch: one LinkedIn post per lesson topic, built from its cheat sheet, two or three times a week.
- Reply to every comment and question in the first weeks. Thank contributors publicly.
- Ask readers to star the repo at natural moments: the home page, the end of each topic, and the progress tracker when they finish a pillar. Never with pop-ups.
- Later: invite community translations (Bengali first) using the same structure.

---

## 11. Full topic and lesson catalog (74 topics: 70 learning topics + 4 Toolbox pages)

Topics and lessons added on 2026-11-15 from the skills matrix gap check (step 0.6) are marked *(added 0.6)*.
Pillar 6, AI-Powered QA, was added by the owner on 2026-11-15 (11 topics; the old Pillar 3 topic "AI in testing" moved into it).

Each row is one topic folder. Its lessons become pages; its templates become files in `modules/`. Examples come from real job situations; the Practice App is optional (owner decision, 2026-11-16).

### Start Here

| Topic | Lessons | Templates |
| --- | --- | --- |
| How to use this site | Learning paths by role; how pages are organized; how to ask for help | — |
| Environment setup | Python, VS Code, virtual environments, Docker (with links out for absolute beginners) | Starter `requirements.txt`; VS Code settings |
| Python for testers *(added 0.6)* | Variables and types; strings, lists and dictionaries; if and loops; functions; modules and imports; classes and objects; errors and exceptions; reading and writing files; JSON; virtual environments and pip; reading other people's Python code | Python practice exercises with tests; starter scripts |
| Practice App tour | What the app does; starting and resetting it; its API docs; its database tables; Bug Hunts (no spoilers) | Practice App; reset script |

### Pillar 1 — Think Like a Tester

| Topic | Lessons | Templates |
| --- | --- | --- |
| Learning a new testing area | How to approach a task you have never done; the 9-step playbook; asking the right questions; reading official docs fast; learning from source code and examples; when to ask for help | Day-one questions checklist; one-page test plan; learning log |
| The SDET role | What an SDET does; SDET vs QA vs developer; skills map; the seven testing principles *(added 0.6)*; the test process and testware *(added 0.6)* | New team onboarding checklist; 30-60-90 day plan; automation readiness checklist *(changed 2026-11-16)* |
| Test levels and the pyramid | Unit, integration, API, UI, end-to-end; the test pyramid; the testing trophy; non-functional test types: performance, usability, compatibility, reliability *(added 0.6)* | Test level decision chart |
| Test design techniques | Equivalence partitioning; boundary values; decision tables; state transitions; pairwise; error guessing; exploratory testing; checklist-based testing *(added 0.6)*; white-box testing: statement and branch coverage *(added 0.6)* | Worksheet per technique; pairwise generator; coverage example |
| Static testing and reviews *(added 0.6)* | What static testing is; reviewing requirements and user stories; finding ambiguity and missing cases; review types (informal, walkthrough, inspection); static analysis tools | Requirements review checklist; user story review worksheet |
| Test cases | Anatomy of a test case; positive and negative cases; traceability | Test case template (Markdown + CSV) |
| Bug reports | What makes a great bug report; severity vs priority; bug lifecycle | Bug report template; GitHub issue form |
| Test strategy and planning | Test strategy; test plan; entry and exit criteria; risk-based testing; what not to automate | Test plan template; automation ROI checklist |

### Pillar 2 — Core Automation

| Topic | Lessons | Templates |
| --- | --- | --- |
| pytest framework | Project layout; tests and asserts; fixtures and `conftest.py`; parametrize; markers; `pytest.ini`; environments | Reusable pytest skeleton |
| API testing | How HTTP works; GET, POST, PUT, PATCH, DELETE; status codes; headers and JSON; query and path params; auth (API key, Basic, Bearer, OAuth2); schema validation; chaining requests; file upload; API client class | One template per method; auth helpers; schema validator; API client |
| Database testing | SQL for testers (SELECT, JOIN, GROUP BY, subqueries); connecting from Python; schema tests; integrity (PK, FK, NOT NULL, UNIQUE); CRUD tests; data validation; stored procedures and triggers; setup and cleanup with transactions | DB client; schema, integrity and CRUD tests; cleanup fixture |
| Multi-database testing | Why test several databases; Docker Compose for MySQL, PostgreSQL, SQLite, MongoDB; config per database; one base client, many drivers; one test on every database with `pytest.mark.parametrize`; cross-database comparison (row counts, checksums, values); migration and ETL validation | Full project: `docker-compose.yml`, `config/databases.yaml`, `config/.env.example`, `db_clients/` (`base_client.py` + one per database), `queries/<database>/`, `test_data/`, `tests/` (`conftest.py`, `test_schema.py`, `test_data_integrity.py`, `test_cross_db_compare.py`) |
| API + database | Verify an API write in the database; seed data then call the API; clean up after | End-to-end API-to-DB test |
| Data-driven testing | Test data from CSV, JSON, YAML and Excel; Faker; factories; keyword-driven testing and Robot Framework *(added 0.6)* | Data loaders; Faker factory; Robot Framework example |
| BDD testing | What BDD is; TDD and ATDD: test-first approaches *(added 0.6)*; Gherkin (Given, When, Then); feature files; step definitions; scenario outlines; tags; hooks; BDD for API; BDD for UI; writing scenarios with the business. Taught fully with **both behave and pytest-bdd**, side by side, equal depth *(decided 0.6)* | behave projects for API and UI; pytest-bdd projects for API and UI (same feature files) |
| UI automation | How browsers and locators work; choosing locators; waits; Page Object Model; forms, alerts, frames, tabs; screenshots on failure; cross-browser runs | Page Object Model framework |
| Reporting and logging | pytest-html; Allure; logging levels; attaching screenshots and request logs | Report config; logging setup |

### Pillar 3 — Advanced Testing

| Topic | Lessons | Templates |
| --- | --- | --- |
| Mocking and stubbing | When to mock; `unittest.mock`; mocking HTTP with `responses`; WireMock | Mock examples; WireMock Docker setup |
| Contract testing | Consumer-driven contracts; Pact basics; contract tests in a pipeline | Pact consumer and provider |
| Testing microservices *(added 0.6)* | How microservices talk; what can break between services; testing one service in isolation; integration tests across services; test environments for many services; distributed tracing for testers | Multi-service Docker Compose test setup; service integration tests |
| Data and ETL testing *(added 0.6)* | What a data pipeline is; source-to-target checks; row counts, checksums and value checks; data quality rules; testing transformations; testing a data warehouse; idempotency and reruns | ETL test framework; data quality checks |
| Flaky tests and speed | Why tests flake; finding and fixing them; retries done right; isolation; parallel runs with `pytest-xdist` | Flaky test detector; parallel config |
| Performance testing | Load, stress, spike and soak; Locust basics; k6 and JMeter *(added 0.6)*; reading results | Locust template; k6 script; JMeter test plan |
| Security testing basics | OWASP Top 10 for testers; auth and permission tests; injection tests; OWASP ZAP scan; testing in regulated fields: HIPAA, PCI DSS, GDPR, SOC 2 *(added 0.6)* | Security checklist; ZAP setup; compliance test checklist |
| Accessibility testing | Why it matters; WCAG basics; axe; manual checks | axe + browser test |
| Visual regression | Comparing screenshots; dynamic content; baselines | Visual test template |
| GraphQL testing | Queries and mutations; schema checks; errors | GraphQL client and tests |
| gRPC and WebSocket testing | How they differ from REST; testing streams and messages | Example tests |
| Message queue testing | Kafka and RabbitMQ basics; producing and consuming test messages; async checks | Kafka test with Docker |
| Mobile testing | Appium basics; emulators and real devices; mobile Page Objects | Appium starter |
| Tricky real-world cases | Email and OTP with Mailpit; file upload and download; PDF content; payment sandboxes; time zones and dates; localization; how teams handle CAPTCHA in tests | Email reader helper; file and PDF checks; date test data |

### Pillar 4 — Infrastructure

| Topic | Lessons | Templates |
| --- | --- | --- |
| CI/CD (teaching topic) | What CI/CD is; GitHub Actions basics; tests on push and pull request; secrets; reports as artifacts; scheduled runs; matrix builds | Workflow templates (as lesson files in `modules/`, not active workflows for this repo until Phase 9) |
| Docker for testers | Images and containers; Dockerfile for a test suite; Docker Compose test environments | Test-runner Dockerfile; compose file |
| Linux and shell | Essential commands; reading logs; grep, tail, pipes; simple scripts | Shell cheat sheet; helper scripts |
| Networking for testers | DNS, IP and ports; HTTPS and certificates; cookies and sessions; CORS; proxies | Network troubleshooting checklist |
| Debugging toolkit | Browser DevTools (Network, Console); curl; reading stack traces; finding root cause | Debugging checklist |
| Everyday tools | Exploring APIs with Postman or Bruno; turning a manual request into a pytest test; VS Code for testers (debugger, breakpoints, extensions); searching large logs | Postman/Bruno collection for the Practice App; VS Code debug config |
| Cloud and Kubernetes basics | Cloud test environments; Kubernetes in plain words; running tests in a cluster | Example Kubernetes job |
| Observability | Logs, metrics, traces; Grafana basics; testing in production; synthetic monitoring | Synthetic check script |

### Pillar 6 — AI-Powered QA *(added by the owner, 2026-11-15; built later, see Phase 7.5)*

Every topic uses the Practice App. Rules for the whole pillar:

- **Never send company code or data to an AI tool your company has not approved.** Every topic repeats this where it matters.
- AI output is a draft. Every topic shows how a person reviews it before it is used.
- Templates call the AI model through one small client class. Each template's tests use a **fake model** that returns fixed answers, so tests run offline, cost nothing, need no API key and always give the same result.
- API keys live only in `.env` (never committed); `.env.example` shows the variable names.
- Which AI provider the examples use is an open decision for when the pillar is built (provider-neutral where possible).

| Topic | Lessons | Templates |
| --- | --- | --- |
| AI basics for testers | What an LLM is, in plain words; prompts and context; tokens and cost; limits; why AI sometimes makes things up (hallucination) and how to catch it | Prompt checklist |
| Using AI coding tools safely | Using Claude Code and Copilot to write test code; giving them the right context; reviewing every line they write; common mistakes they make; what never to paste in | Review checklist for AI-written code; safe-use rules |
| Prompting for QA | Test ideas from a feature; test cases from requirements; bug report drafts; edge cases you missed; prompt patterns that work | Prompt library for QA tasks |
| AI test generation | Tests from an OpenAPI spec; tests from a user story; checking generated tests (do they run, do they test the right thing, do they fail when they should) | Spec-to-tests generator with a review step |
| Building your first QA agent | What an agent is; a small Python agent that runs pytest, reads the failures and writes a summary; tools, loops and stopping safely | Minimal QA agent with tests (fake model) |
| Orchestrating agents | A generate → run → triage → report pipeline; passing results between steps; a person approving the key steps; logging what every agent did | Agent pipeline with human approval gates |
| AI for bug detection and triage | Reading logs; grouping similar failures; spotting duplicate bugs and flaky tests; when to trust it and when not to | Failure clustering and duplicate finder |
| Smarter regression and self-healing locators | AI-assisted choice of which tests to run for a change; "self-healing" locators; their risks (hiding real bugs, silent changes) and safe limits | Regression selector; locator healing with an audit log |
| AI-written reports and release summaries | Test summary reports; release notes; making them accurate (facts from data, not guesses); a person signs off | Report generator from pytest results |
| Testing AI features | Testing features built on AI models; evals; checking unpredictable output; safety and harmful output; prompt injection; regression for model changes *(moved from Pillar 3)* | AI output evaluation template; eval suite starter |
| Measuring AI's impact, and the rules | Measuring time saved and quality honestly; cost; privacy and data rules; company approval; never sending company code to unapproved tools; writing a team AI policy | Impact measurement sheet; team AI usage policy |

### Pillar 5 — The Professional SDET

| Topic | Lessons | Templates |
| --- | --- | --- |
| A day in the life | From ticket to test to bug report; stand-up; reviewing pull requests; release day | Daily checklist |
| Your first weeks in a new job | Reading a framework someone else wrote; mapping the system; questions to ask; your first useful pull request; building trust | 30-60-90 day plan; framework reading checklist |
| SDET in Agile | SDLC models: Waterfall, V-model, iterative, Agile, DevOps *(added 0.6)*; Scrum and Kanban; user stories and acceptance criteria; Three Amigos; shift-left; definition of done | Acceptance criteria template |
| Git in a team | Branching workflow; good pull requests; reviewing test code; merge conflicts; staying up to date | PR template; review checklist |
| Jira and test management | Tickets and workflows; linking tests to stories; test runs | Jira bug template |
| Working with developers | Talking about bugs without blame; code review for test code; pairing | Code review checklist |
| Regression, hotfixes and incidents | Smoke vs regression suites; tagging; choosing tests for a change; testing a hotfix under pressure; root cause analysis; blameless postmortems | Tagging setup; hotfix checklist; postmortem template |
| Communicating your work | Estimating test effort; daily status updates; test summary reports; explaining risk to managers; demos | Estimation sheet; status update; test summary report |
| Quality metrics | Coverage; defect leakage; flaky rate; lead time; what not to measure | Metrics dashboard example |
| Release sign-off | Go / no-go decisions; release checklists; smoke tests after deploy | Release checklist |
| Clean test code | Naming; structure; DRY vs readable; ruff; type hints; design patterns for tests; testing your own test framework *(added 0.6)* | Lint config; framework self-tests |
| Leading quality (senior level) | Designing test architecture; choosing a test automation tool *(added 0.6)*; quality strategy for a team; building shared test tools; continuous improvement of automation *(added 0.6)*; mentoring; influencing without authority; interviewing testers | Quality strategy; architecture decision record; tool comparison matrix; mentoring plan |
| Capstone project | A full framework against the Practice App: API, DB, UI, BDD, reports, Docker, CI | Complete capstone |
| Career roadmap | Junior, mid, senior, lead: what each level knows and does; which languages job ads ask for, and reading a little TypeScript and Java *(added 0.6)* | Skills checklist per level |
| Interview preparation | Common questions; coding challenges; take-home tasks; system design for testers | Question bank with answers |
| Portfolio and resume | What to show on GitHub; a tester resume; LinkedIn profile | Resume template |

### Toolbox — quick reference

| Topic | Pages | Contents |
| --- | --- | --- |
| Cheat sheets | SQL; pytest commands; HTTP methods and status codes; Git; Linux; locators; Gherkin; Docker | One printable page each, also as a shareable image |
| Test idea banks | Login; sign-up; search; cart and checkout; payments; bank transfer; file sharing; notifications; user roles and permissions | Ready lists of what to test for each feature type |
| Template index | Every template on the site | Name, topic, what it does, link to the file |
| Glossary | Every testing term on the site | Plain-English meaning, link to the lesson |

---

## 12. Build roadmap

Work through the phases in order. Do not start a phase until the one before it has passed its gate and I have approved it.

### Phase 0 — Clean up and decide

- 0.1 Inventory every file in the repo; suggest keep / move / rewrite / delete for each.
- 0.2 Make the old repository private and rename it `python-sdet-practice-archive`. It is never made public again, because its history contains a real password.
- 0.3 Scan files and git history for secrets and personal data; report findings; help me remove them and remind me to change any exposed password.
- 0.4 Confirm the open decisions in section 14.
- 0.5 Create the new **private** repository `zero-to-sdet` with a fresh history. Turn on gitleaks pre-commit before the first commit. Copy in only the files I approved in 0.1, as new files (never copy the old git history). Set the description and topics from section 1.
- 0.6 Build the skills matrix (section 2, core idea 3) from the catalog, 30+ job ads and public syllabi. Report every gap.

Gate: clean `main`, no secrets, decisions written down.

### Phase 1 — Foundation (local only)

- 1.1 Create the folder skeleton from section 5, with placeholder pages for every tab.
- 1.2 Install Zensical; write `zensical.toml` (name, author, colors, light/dark, tabs, search, code copy).
- 1.3 Turn on Markdown features: admonitions, tabs, collapsible blocks, Mermaid, snippet includes, task lists, tags.
- 1.4 Preview locally with `zensical serve` (publishing comes in Phase 9).
- 1.5 Home page: hero, "I need to…" task finder, learning paths by role, pillar cards, star button.
- 1.6 Learning Path page with a Mermaid diagram.
- 1.7 About page and footer with my name.
- 1.8 Giscus comments and the feedback widget.
- 1.9 Help me turn on GitHub Discussions (Q&A, Ideas, Show and tell).
- 1.10 `STYLE_GUIDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, issue and PR templates.
- 1.11 `_new_topic_template/`; test it by creating one dummy topic, then remove the dummy.
- 1.12 `scripts/check.sh` and `.pre-commit-config.yaml`: tests, link check, ruff, gitleaks.
- 1.13 README: banner, badges, screenshot, topic map, "I need to…" list.
- 1.14 Glossary, Tags and Start Here pages.
- 1.15 Progress tracker (saved in the reader's browser only) and the skills matrix page.
- 1.16 Add the readability check to `scripts/check.sh`.
- 1.17 Automatic share image for every page, share buttons, and the credit-line rule in `_new_topic_template/`.

Gate: the site runs locally, looks finished with placeholders, and a new topic can be added in under 10 minutes.

### Phase 1.5 — The Practice App

- 1.5.1 Feature list and data model diagram.
- 1.5.2 API: auth, users, products, search, cart, checkout, orders, admin.
- 1.5.3 PostgreSQL + MySQL reporting copy, Faker seed data.
- 1.5.4 Simple web page: log in, product list, cart, checkout.
- 1.5.5 Email and OTP through Mailpit; file upload and download.
- 1.5.6 `docker compose up`, reset script, health check page, GitHub Codespaces setup (`.devcontainer/`) with an "Open in Codespaces" button, and a guard that stops the app from starting on a non-local address while it still has the fake default passwords.
- 1.5.7 Plant a starter set of bugs (about 6); write the hidden answers page. The other bugs come with the topics that use them.
- 1.5.8 One short Practice App tour page.

Gate: the app starts with one command on a clean macOS, Windows and Linux machine.

### Phase 2 — Pillar 1: Think Like a Tester

Build every Pillar 1 topic from section 11, starting with **Learning a new testing area** (every later topic uses its playbook method). Pillar 1 includes **Static testing and reviews**.

Also build **Python for testers** (Start Here) in this phase, so readers can code before Phase 3.

Gate: every page meets the definition of done.

### Phase 3 — Pillar 2: Core Automation

In this order: pytest framework → API testing → Database testing → Multi-database testing → API + database → Data-driven testing → BDD testing → UI automation → Reporting and logging.

Gate: all templates pass locally with `scripts/check.sh`.

### Phase 4 — Pillar 4: Infrastructure (first part)

CI/CD (teaching topic) → Docker for testers → Linux and shell → Networking → Debugging toolkit → Everyday tools.

Gate: a reader can run the whole suite locally and in Docker.

### Phase 5 — Pillar 5 essentials, Toolbox and polish

- A day in the life; Your first weeks in a new job; SDET in Agile; Git in a team; Working with developers; Regression, hotfixes and incidents; Communicating your work.
- Toolbox: cheat sheets, test idea banks, template index.
- Polish: complete `IMAGES_NEEDED.md` with me; check every page on mobile; run the link check.
- Social preview image and per-topic cheat sheet images.
- Draft the launch posts.
- Get feedback from 3–5 trusted testers on a local preview.

Gate: the first pillars are complete and reviewed.

### Phase 6 — Pillar 3: Advanced Testing

Mocking → Contract → Testing microservices → Data and ETL testing → Flaky tests and speed → Performance → Security → Accessibility → Visual regression → GraphQL → gRPC and WebSocket → Message queues → Mobile → Tricky real-world cases. ("AI in testing" moved to Pillar 6.)

Gate: every topic meets the definition of done.

### Phase 7 — Cloud, observability and the capstone

Cloud and Kubernetes basics → Observability → Quality metrics → Release sign-off → Clean test code → Jira and test management → Capstone project.

### Phase 7.5 — Pillar 6: AI-Powered QA *(added 2026-11-15)*

Built after the core skills it uses (pytest, API, CI, reports) and before the career phase.
AI basics for testers → Using AI coding tools safely → Prompting for QA → AI test generation → Building your first QA agent → Orchestrating agents → AI for bug detection and triage → Smarter regression and self-healing locators → AI-written reports and release summaries → Testing AI features → Measuring AI's impact, and the rules.

First step of the phase: decide the AI provider for the examples, add the new section and its "Coming soon" pages, add its skills to the skills matrix, and add its terms (LLM, prompt, hallucination, agent, eval...) to the Glossary.

Gate: every topic meets the definition of done; every template test passes offline with the fake model.

### Phase 8 — Career and senior level

Career roadmap → Interview preparation → Portfolio and resume → Leading quality (senior level) → v1.0 changelog and launch announcement.

Also in this phase: the SDET Skills Assessment quiz and result card, the capstone "Built with Zero to SDET" badge, the interview question issue form, and the Bug Hunt Hall of Fame.

### Phase 9 — Final review, security audit, CI/CD and launch

- 9.1 Full content review of every page against the definition of done.
- 9.1b Final coverage check: every skill in the skills matrix links to a finished lesson; re-check against fresh job ads.
- 9.2 Security audit: every rule in section 9.
- 9.3 Full git history scan with gitleaks; fix anything found before going public.
- 9.4 Help me turn on GitHub secret scanning with push protection, Dependabot alerts, 2FA, and branch protection on `main`.
- 9.4b Make `zero-to-sdet` **public** (section 3A, Stage 2). Only after 9.1–9.4 pass.
- 9.5 Add `.github/workflows/run-tests.yml` (all template tests on push and pull request).
- 9.6 Add `.github/workflows/deploy-site.yml` (build and publish to GitHub Pages).
- 9.7 Add `.github/workflows/check-links.yml` (weekly).
- 9.8 Publish; check every page on phone and desktop.
- 9.9 Tag release v1.0.
- 9.10 Launch posts, cheat sheet images, share images and the README demo GIF (section 10 growth plan).

Gate: v1.0 is public, secure and announced. Every new topic after this follows the same definition of done and ships with a release note.

---

## 13. Definition of done

**A lesson is done when:**

- [ ] It follows the lesson template (7.2), including the "Before you start" box, so it makes sense on its own
- [ ] A reader who runs nothing can still learn everything from the page: every step shows its real output or a screenshot (7.3)
- [ ] It follows the writing style (section 8) and was read aloud once
- [ ] It has at least one diagram, and a screenshot or output block for every step (or a listed placeholder)
- [ ] Every code sample runs, comes from `modules/`, and has a passing test
- [ ] It has common mistakes, "if you see this error", an exercise with a solution, a quick check, and a References list
- [ ] Every new term is in the Glossary and linked
- [ ] It looks right on phone and desktop, in light and dark mode
- [ ] All links work
- [ ] It is in the navigation, with tags, level badge, and previous / next links
- [ ] Comments and the feedback widget show at the bottom
- [ ] It passes the security rules (section 9)
- [ ] It passes the 10-year-old test (section 8A) and the readability check
- [ ] It is linked from the skills matrix

**A topic is done when** all its lessons are done, its templates pass locally, its index page is a complete "First time? Start here" playbook with "Jump to what you need" and "Official resources", and it has a Bug Hunt against the Practice App.

---

## 14. Open decisions (ask me before Phase 1)

| Decision | Options | Suggested default |
| --- | --- | --- |
| Author name on the site | Decided | Arshaduzzaman SM |
| Repo name | Decided | `zero-to-sdet` |
| GitHub username | Decided | `arshaduzzaman-sm` |
| LinkedIn link | Decided | Yes: https://www.linkedin.com/in/arshaduzzaman-sm/ |
| Main color | Decided | Calm blue |
| UI automation tool | Decided | **Playwright only.** No Selenium pages or templates. |
| BDD tool | Decided | **Both behave and pytest-bdd, equal depth.** No main and no side track: full lessons and full templates for each (section 2, "Equal depth"). |
| Multi-database set | Decided | MySQL, PostgreSQL, SQLite, MongoDB |
| Custom domain | Decided | GitHub Pages first; own domain later (section 3A) |
| Analytics | Decided | GoatCounter (free, no cookies, no cookie banner). Account created in Phase 9. |

---

*Start now with section 0, step 1: read the repository and report back. Do not change anything yet.*

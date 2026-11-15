# Contributing to Zero to SDET

Thank you for helping. Every fix, however small, makes the site better for the
next learner.

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to help

| You want to | Do this |
| --- | --- |
| Fix a typo or a small mistake | Click **Edit this page** (the pencil at the top of any page), change it on GitHub, open a pull request |
| Report something wrong or unclear | Click 👎 under "Was this page helpful?" on the page, or open a **Content error** issue |
| Report a template that does not run | Open a **Template or code problem** issue |
| Report a security problem | Never in a public issue. See [SECURITY.md](SECURITY.md) |
| Add or rewrite a lesson | Read this whole page and the [Style guide](STYLE_GUIDE.md) first |

## Set up your computer

You need [uv](https://docs.astral.sh/uv/) (it installs the right Python for you) and git.

```bash
git clone https://github.com/arshaduzzaman-sm/zero-to-sdet.git
cd zero-to-sdet

uv python install 3.13
uv venv --python 3.13
uv pip sync --require-hashes requirements-docs.txt requirements.txt

uv tool install pre-commit
pre-commit install            # runs gitleaks and the other checks before every commit

.venv/bin/zensical serve      # then open http://127.0.0.1:8001/zero-to-sdet/
```

`--require-hashes` makes sure every package is exactly the one that was reviewed.

## Add a new topic

A topic is a folder in a section, for example `docs/core-automation/api-testing/`.
The menu and the section overview cards are **built from the topic's own front
matter**, so there is no list to edit by hand.

**The quick way (recommended):** one command makes the page, the code folders
and the menu entry. It checks the section, group and name for you.

```bash
.venv/bin/python scripts/new_topic.py --section core-automation --slug api-testing \
  --title "API testing" --level Intermediate --group "API and databases" \
  --after pytest-framework --summary "Send requests from Python and check the answers."
```

When you start writing the real pages, copy them from
[`_new_topic_template/`](_new_topic_template/README.md).

**By hand**, if you prefer:

1. Pick the section and a short folder name: lowercase, words joined with `-`,
   **no numbers** (the order lives in the front matter).
2. Create `docs/<section>/<topic>/index.md` with this front matter:

    ```yaml
    ---
    title: "API testing"
    description: "One or two sentences for search engines and link previews."
    level: Intermediate                 # Beginner, Intermediate, Advanced or Senior
    status: draft                       # remove when the topic is finished
    tags:
      - core-automation
    nav_title: "API testing"            # short label in the menu
    order: 25                           # between the topics at 20 and 30
    group: "API and databases"          # only if the section uses groups
    summary: "One plain sentence for the card on the section overview."
    ---
    ```

3. Make the same folder in `modules/` for the code (underscores instead of `-`,
   for example `modules/core_automation/api_testing/`). See [modules/README.md](modules/README.md).
4. Build the menu and the overview cards:

    ```bash
    .venv/bin/python scripts/build_nav.py
    ```

5. Check the site builds with no warnings:

    ```bash
    .venv/bin/zensical build --strict
    ```

If you forget step 4, the commit stops with "menu and overview pages are up to
date ... Failed" and tells you the command to run.

**Lessons** inside a topic are more `.md` files in the topic folder, each with
`nav_title` and `order`. They appear under the topic in the menu automatically.

**Published addresses never change.** If a page must move, add a redirect.

## Check everything before you push

One command runs every check (secrets, Python lint and format, menu, site build,
links, tests, readability) and prints a summary:

```bash
scripts/check.sh              # about 10 seconds
scripts/check.sh --external   # also visits every external link
```

## Before you open a pull request

A lesson is done when:

- [ ] It follows the lesson template ([Style guide 7.2](STYLE_GUIDE.md#72-lesson-page-template-top-to-bottom)), including the "Before you start" box, so it makes sense on its own
- [ ] It follows the writing style ([Style guide 8](STYLE_GUIDE.md#8-writing-style)) and was read aloud once
- [ ] It has at least one diagram, and a screenshot or output block for every step (or a placeholder listed in `docs/assets/images/IMAGES_NEEDED.md`)
- [ ] Every code sample runs, comes from `modules/`, and has a passing test
- [ ] It has common mistakes, "if you see this error", an exercise with a solution, a quick check, and a References list
- [ ] Every new term is in the Glossary and linked
- [ ] It looks right on phone and desktop, in light and dark mode
- [ ] All links work
- [ ] It is in the menu (`scripts/build_nav.py`), with tags and a level
- [ ] It passes the [security rules](SECURITY.md)
- [ ] It passes the 10-year-old test ([Style guide 8A](STYLE_GUIDE.md#8a-the-10-year-old-test))
- [ ] It is linked from the [Skills Matrix](docs/start-here/skills-matrix.md)

A topic is done when all its lessons are done, its templates pass locally, its
`index.md` is a complete "First time? Start here" playbook, and it has a Bug Hunt
against the Practice App.

## Pull requests

- One topic or one fix per pull request, so it is easy to review.
- Say what changed, why, and how to check it (the template asks for this).
- Never include passwords, tokens, real emails, personal paths or employer material.

## Licenses

By contributing you agree that your code is shared under the [MIT License](LICENSE)
and your text and images under [CC BY 4.0](LICENSE-CC-BY-4.0.txt), the same as the
rest of the project.

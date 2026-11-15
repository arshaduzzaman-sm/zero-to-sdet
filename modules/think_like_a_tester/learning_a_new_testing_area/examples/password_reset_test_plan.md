# Test plan: password reset in the Practice App

Author: Arshad · Reviewed by: team lead · Date: 2026-11-15

## 1. What and why

Test the "forgot password" flow of the Bookshelf shop: ask for a code, get it by
email, set a new password. A broken reset can lock users out, or let someone
else take over an account.

## 2. In scope and out of scope

| In scope | Out of scope |
| --- | --- |
| `POST /api/auth/forgot-password` and `POST /api/auth/reset-password` | Sign-up codes (tested next sprint) |
| The reset email in Mailpit | Real email delivery |
| The web pages `/forgot-password` and `/reset-password` | Load and speed |

## 3. Risks (highest first)

| Risk | Why it matters | How I will test it |
| --- | --- | --- |
| An old or used code still works | Someone with an old email could take over the account | Use a code after 10 minutes (move the app clock), and use it twice |
| The answer shows whether an email has an account | Attackers learn who uses the shop | Ask for a code for a known and an unknown email; compare the answers |
| A wrong code can be guessed | Six digits can be guessed with enough tries | Send 5 wrong codes, then the right one |
| The new password is weak | Weak passwords are easy to guess | Try a short password and one without a digit |

## 4. Approach

- Test levels: API first (fast and exact), then one web test for the happy path.
- Techniques: boundary values (exactly 10 minutes), negative cases, error guessing.
- Tools: pytest with requests, Mailpit's API to read the code, the admin clock.
- Test data: the seed user `arshad`; reset with `python -m bookshelf reset` after each run.

## 5. Environments and access

The Practice App on my computer (`docker compose up -d`). Admin login for the clock.

## 6. Done when

- [ ] Every high risk has at least one test
- [ ] All tests pass, or every failure has a bug report
- [ ] The plan and the results are shared with the team lead

## 7. Open questions

- Should a new code cancel the older ones? (Asked the developer; waiting.)

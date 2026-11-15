# Practice App: Bookshelf

A small online shop with bugs planted on purpose. Every lesson on
[Zero to SDET](https://arshaduzzaman-sm.github.io/zero-to-sdet/) tests this app.

> [!WARNING]
> For practice on your own computer only. Every service listens on `localhost`.
> Never deploy it to the internet.

**Status:** being built in Phase 1.5. The web shop, the API, the databases,
email (Mailpit), picture uploads and invoice PDFs work now. A one-command start
comes in the next step. The plan, features and data model are in
[DESIGN.md](DESIGN.md).

## Start it without Docker

You need Python 3.13 and the project set up as in
[CONTRIBUTING.md](../CONTRIBUTING.md). Then, from the repository root:

```bash
cd practice-app
../.venv/bin/python -m bookshelf
```

Open <http://127.0.0.1:8080> for the shop, or <http://127.0.0.1:8080/docs> for
the API (you can try every endpoint in the browser). Press `Ctrl+C` to stop the app.

The data lives in `practice-app/data/bookshelf.db` (a SQLite file, never
committed). Delete that file, or call `POST /api/admin/reset`, to start fresh.
When a new version of the app changes the tables, it rebuilds this practice data
from the seed on its next start (the terminal says so).

## Start it with Docker (the real databases)

With Docker, the app uses three databases, as many real projects do:
PostgreSQL (main), MySQL (a reporting copy, refreshed every minute) and MongoDB
(reviews), plus Mailpit for email. You need
[Docker Desktop](https://docs.docker.com/get-started/get-docker/).

```bash
cd practice-app
cp .env.example .env          # then remove the # in front of the *_URL and SMTP_* lines
docker compose up -d          # start the databases and Mailpit (the first time downloads them)
../.venv/bin/python -m bookshelf
```

Connect to the databases with any client, from your own computer only:

| Database | Address | User | Password | Database name |
| --- | --- | --- | --- | --- |
| PostgreSQL | `127.0.0.1:55432` | `bookshelf` | `local_only_password` | `bookshelf` |
| MySQL | `127.0.0.1:53306` | `bookshelf` | `local_only_password` | `reporting` |
| MongoDB | `127.0.0.1:57017` | `bookshelf` | `local_only_password` | `bookshelf` (auth database: `admin`) |

`docker compose down` stops them (your data stays). `docker compose down -v`
also deletes the data.

## Logins to try

| Username | Password | Role |
| --- | --- | --- |
| `arshad` | `Test@1234` | customer |
| `maria` | `Test@1234` | customer |
| `admin` | `local_only_password` | admin |

All fake. There are also 40 customers made by Faker (password `Test@1234` too),
with orders and reviews. The data is the same on every computer. To change any
of this, copy `.env.example` to `.env` and edit it.

## Emails and sign-up codes

The app sends a sign-up code, a password reset code and an order confirmation.

- **With Docker:** open Mailpit at <http://127.0.0.1:58025> to read every email.
  Nothing reaches a real inbox. Tests can read them with Mailpit's API, for
  example `http://127.0.0.1:58025/api/v1/search?query=to:you@example.com`.
- **Without Docker:** every email is printed in the terminal where the app runs,
  and saved as a text file in `practice-app/data/outbox/`.

## Pictures and invoices

- **Profile picture:** on <http://127.0.0.1:8080/profile>, or `POST /api/users/me/avatar`.
- **Product image (admin):** on the admin page, or `POST /api/products/{id}/image`.
- Send the file as form data in a field named `file`: JPEG or PNG, up to 2 MB.
  Anything else gets a clear error (good practice for negative tests).
- **Invoice PDF:** on an order page, "Download invoice (PDF)", or
  `GET /api/orders/{id}/invoice.pdf`.

## Sandbox cards

| Card number | What happens |
| --- | --- |
| `4242 4242 4242 4242` | Payment succeeds |
| `4000 0000 0000 0002` | Declined (402) |
| `4000 0000 0000 9995` | Times out (504, after 3 seconds) |

Any expiry date in the future (`12/30`) and any 3-digit CVC (`123`).

## The app's own tests

```bash
.venv/bin/pytest practice-app/tests
```

These check the app itself. They are not the lesson templates: lessons teach
you to write your own tests against the running app.

By default they use throwaway SQLite databases. To run them against the Docker
databases, set `BOOKSHELF_TEST_DATABASE_URL`, `BOOKSHELF_TEST_REPORTING_URL` and
`BOOKSHELF_TEST_MONGODB_URL` (see `tests/conftest.py`). Careful: this resets
the data in those databases. To also check real Mailpit, set
`BOOKSHELF_TEST_MAILPIT=127.0.0.1:51025:58025`.

# Practice App: Bookshelf

A small online shop with bugs planted on purpose. Every lesson on
[Zero to SDET](https://arshaduzzaman-sm.github.io/zero-to-sdet/) tests this app.

> [!WARNING]
> For practice on your own computer only. Every service listens on `localhost`.
> Never deploy it to the internet.

**Status:** being built in Phase 1.5. The API works now. Web pages, Docker,
email (Mailpit) and file uploads come in the next steps. The plan, features
and data model are in [DESIGN.md](DESIGN.md).

## Start it without Docker

You need Python 3.13 and the project set up as in
[CONTRIBUTING.md](../CONTRIBUTING.md). Then, from the repository root:

```bash
cd practice-app
../.venv/bin/python -m bookshelf
```

Open <http://127.0.0.1:8080/docs>. Every endpoint is there, and you can try
each one in the browser. Press `Ctrl+C` to stop the app.

The data lives in `practice-app/data/bookshelf.db` (a SQLite file, never
committed). Delete that file, or call `POST /api/admin/reset`, to start fresh.

## Logins to try

| Username | Password | Role |
| --- | --- | --- |
| `arshad` | `Test@1234` | customer |
| `maria` | `Test@1234` | customer |
| `admin` | `local_only_password` | admin |

All fake. To change them, copy `.env.example` to `.env` and edit it.

## Sign-up codes

Until Mailpit is added, every email (sign-up code, password reset code, order
confirmation) is printed in the terminal where the app runs, and saved as a
text file in `practice-app/data/outbox/`.

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

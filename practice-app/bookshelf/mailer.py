"""Emails the app sends (sign-up code, password reset code, order confirmation).

Until Mailpit is added (step 1.5.5), every email is printed to the console and
saved as a text file in practice-app/data/outbox/, so you can read the code.
Tests read them from `Outbox.sent`.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

log = logging.getLogger("bookshelf.email")


@dataclass
class Email:
    to: str
    subject: str
    body: str
    sent_at: datetime


class Outbox:
    def __init__(self, folder: Path | None = None) -> None:
        self.folder = folder
        self.sent: list[Email] = []

    def send(self, to: str, subject: str, body: str, now: datetime) -> Email:
        email = Email(to, subject, body, now)
        self.sent.append(email)
        log.info("Email to %s | %s | %s", to, subject, " ".join(body.split()))
        if self.folder is not None:
            self.folder.mkdir(parents=True, exist_ok=True)
            safe_to = re.sub(r"[^A-Za-z0-9@._-]", "_", to)
            name = f"{now.strftime('%Y%m%dT%H%M%S%f')}-{safe_to}.txt"
            text = f"To: {to}\nSubject: {subject}\nDate: {now.isoformat()}\n\n{body}\n"
            (self.folder / name).write_text(text, encoding="utf-8")
        return email

    def last_to(self, to: str) -> Email | None:
        for email in reversed(self.sent):
            if email.to == to:
                return email
        return None

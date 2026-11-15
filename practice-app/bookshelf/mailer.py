"""Emails the app sends (sign-up code, password reset code, order confirmation).

- With SMTP_HOST set, every email goes to that SMTP server. Locally that is
  Mailpit: it catches every email (nothing reaches a real inbox) and shows them
  at http://127.0.0.1:58025. Tests can read them with Mailpit's own API.
- Without SMTP_HOST, every email is printed in the terminal and saved as a
  text file in practice-app/data/outbox/.

A failed send is logged, never shown to the user as a crash: the user can ask
for a new code. Tests read every email from `Outbox.sent`.
"""

from __future__ import annotations

import logging
import re
import smtplib
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from email.utils import format_datetime, make_msgid
from pathlib import Path

log = logging.getLogger("bookshelf.email")


@dataclass
class Email:
    to: str
    subject: str
    body: str
    sent_at: datetime


class Outbox:
    def __init__(
        self,
        folder: Path | None = None,
        smtp_host: str = "",
        smtp_port: int = 1025,
        mail_from: str = "Bookshelf <no-reply@bookshelf.example>",
    ) -> None:
        self.folder = folder
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.mail_from = mail_from
        self.sent: list[Email] = []

    @property
    def mode(self) -> str:
        return "smtp" if self.smtp_host else "console"

    def send(self, to: str, subject: str, body: str, now: datetime) -> Email:
        email = Email(to, subject, body, now)
        self.sent.append(email)
        if self.smtp_host:
            self._send_smtp(email)
        else:
            self._save_locally(email)
        return email

    def _send_smtp(self, email: Email) -> None:
        message = EmailMessage()
        message["From"] = self.mail_from
        message["To"] = email.to
        message["Subject"] = email.subject
        message["Date"] = format_datetime(email.sent_at)
        message["Message-ID"] = make_msgid(domain="bookshelf.example")
        message.set_content(email.body)
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=5) as server:
                server.send_message(message)
            log.info("Email to %s sent to %s:%s | %s", email.to, self.smtp_host,
                     self.smtp_port, email.subject)  # fmt: skip
        except (OSError, smtplib.SMTPException) as error:
            log.warning("Could not send the email to %s (%s). Is Mailpit running?", email.to, error)

    def _save_locally(self, email: Email) -> None:
        log.info("Email to %s | %s | %s", email.to, email.subject, " ".join(email.body.split()))
        if self.folder is not None:
            self.folder.mkdir(parents=True, exist_ok=True)
            safe_to = re.sub(r"[^A-Za-z0-9@._-]", "_", email.to)
            name = f"{email.sent_at.strftime('%Y%m%dT%H%M%S%f')}-{safe_to}.txt"
            text = (
                f"To: {email.to}\nSubject: {email.subject}\n"
                f"Date: {email.sent_at.isoformat()}\n\n{email.body}\n"
            )
            (self.folder / name).write_text(text, encoding="utf-8")

    def is_up(self) -> str:
        """'up' or 'down' for the SMTP server; 'console' when emails are only printed."""
        if not self.smtp_host:
            return "console"
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=2) as server:
                server.noop()
            return "up"
        except (OSError, smtplib.SMTPException):
            return "down"

    def last_to(self, to: str) -> Email | None:
        for email in reversed(self.sent):
            if email.to == to:
                return email
        return None

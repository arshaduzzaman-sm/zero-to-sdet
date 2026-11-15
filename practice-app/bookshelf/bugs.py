"""The Bug Hunt switch.

The Practice App has bugs planted on purpose, for the Bug Hunts at the end of
each topic. They are on by default. PRACTICE_APP_BUGS=off turns every one of
them off, so a lesson can show what the correct behavior looks like.

The answers are in practice-app/BUG_HUNT_ANSWERS.md. Try the Bug Hunt first:
reading this code to find them skips the practice.
"""

from __future__ import annotations

_on = True


def switch(on: bool) -> None:
    global _on  # noqa: PLW0603  (one switch for the whole app)
    _on = on


def on(code: str) -> bool:  # noqa: ARG001  (the code names the answer in BUG_HUNT_ANSWERS.md)
    return _on

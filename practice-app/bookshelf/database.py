"""Create the tables, load the seed data, and reset everything."""

from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy import func, select

from .db import Base
from .models import User
from .seed import seed


def prepare(app: FastAPI) -> None:
    """On start: make missing tables, and seed an empty database."""
    engine = app.state.engine
    Base.metadata.create_all(engine)
    with app.state.sessionmaker() as session:
        if not session.scalar(select(func.count(User.id))):
            seed(session, app.state.settings, app.state.hasher)


def reset_data(app: FastAPI) -> None:
    engine = app.state.engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with app.state.sessionmaker() as session:
        seed(session, app.state.settings, app.state.hasher)

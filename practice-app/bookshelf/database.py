"""Create the tables, load the seed data, keep the reporting copy, reset everything."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from sqlalchemy import Engine, Table, func, inspect, select

from . import files, reporting
from .db import Base
from .models import User
from .seed import seed


def main_tables(app: FastAPI) -> list[Table]:
    """Every table of the main database. With MongoDB, reviews are not a table."""
    tables = Base.metadata.sorted_tables
    if app.state.settings.mongodb_url:
        tables = [table for table in tables if table.name != "reviews"]
    return tables


log = logging.getLogger("bookshelf")


def outdated(engine: Engine, tables: list[Table]) -> list[str]:
    """Tables that exist but miss columns the code needs (an older app version made them)."""
    existing = inspect(engine)
    names = set(existing.get_table_names())
    old = []
    for table in tables:
        if table.name in names:
            have = {column["name"] for column in existing.get_columns(table.name)}
            if not {column.name for column in table.columns} <= have:
                old.append(table.name)
    return old


def prepare(app: FastAPI) -> None:
    """On start: make missing tables, seed an empty database, fill the reporting copy.

    If the database was made by an older version of the app (missing columns), it is
    rebuilt from the seed data: this is practice data, and a clear start is better than
    a crash.
    """
    old = outdated(app.state.engine, main_tables(app)) + outdated(
        app.state.reporting_engine, reporting.ReportingBase.metadata.sorted_tables
    )
    if old:
        log.warning("The database is from an older app version (%s). Rebuilding it from the "
                    "seed data.", ", ".join(sorted(set(old))))  # fmt: skip
        reset_data(app)
        return
    Base.metadata.create_all(app.state.engine, tables=main_tables(app))
    reporting.ReportingBase.metadata.create_all(app.state.reporting_engine)
    with app.state.sessionmaker() as session:
        if not session.scalar(select(func.count(User.id))):
            app.state.reviews.clear()
            seed(session, app.state.settings, app.state.hasher, app.state.reviews)
    sync_reporting(app)


def sync_reporting(app: FastAPI) -> dict:
    return reporting.sync(
        app.state.sessionmaker, app.state.reporting_sessionmaker, app.state.clock.now()
    )


def reset_data(app: FastAPI) -> None:
    tables = main_tables(app)
    Base.metadata.drop_all(app.state.engine, tables=tables)
    Base.metadata.create_all(app.state.engine, tables=tables)
    reporting.ReportingBase.metadata.drop_all(app.state.reporting_engine)
    reporting.ReportingBase.metadata.create_all(app.state.reporting_engine)
    app.state.reviews.clear()
    files.remove_all(app.state.settings.files_dir)
    with app.state.sessionmaker() as session:
        seed(session, app.state.settings, app.state.hasher, app.state.reviews)
    sync_reporting(app)

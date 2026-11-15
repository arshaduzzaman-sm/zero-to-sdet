"""Create the tables, load the seed data, keep the reporting copy, reset everything."""

from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy import Table, func, select

from . import reporting
from .db import Base
from .models import User
from .seed import seed


def main_tables(app: FastAPI) -> list[Table]:
    """Every table of the main database. With MongoDB, reviews are not a table."""
    tables = Base.metadata.sorted_tables
    if app.state.settings.mongodb_url:
        tables = [table for table in tables if table.name != "reviews"]
    return tables


def prepare(app: FastAPI) -> None:
    """On start: make missing tables, seed an empty database, fill the reporting copy."""
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
    with app.state.sessionmaker() as session:
        seed(session, app.state.settings, app.state.hasher, app.state.reviews)
    sync_reporting(app)

"""Where reviews are kept.

With Docker they live in MongoDB (a document database), so lessons can test
SQL and NoSQL side by side. Without Docker they live in the `reviews` table of
the main database. Both stores behave the same; the API does not know which
one it uses.

A review is a plain dict:
    {"id": "...", "product_id": 2, "user_id": 1, "username": "arshad",
     "rating": 5, "text": "...", "created_at": datetime (UTC)}
"""

from __future__ import annotations

from datetime import UTC
from typing import Protocol

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .models import Review


class DuplicateReviewError(Exception):
    """This customer has already reviewed this product."""


class ReviewStore(Protocol):
    def list_for(self, product_id: int) -> list[dict]: ...
    def stats(self, product_ids: list[int]) -> dict[int, tuple[float, int]]: ...
    def exists(self, product_id: int, user_id: int) -> bool: ...
    def add(self, review: dict) -> dict: ...
    def add_many(self, reviews: list[dict]) -> None: ...
    def clear(self) -> None: ...
    def is_up(self) -> bool: ...


def _average(total: float, count: int) -> float:
    return round(total / count, 2)


class SqlReviews:
    def __init__(self, make_session: sessionmaker) -> None:
        self.make_session = make_session

    @staticmethod
    def _as_dict(row: Review) -> dict:
        return {
            "id": str(row.id),
            "product_id": row.product_id,
            "user_id": row.user_id,
            "username": row.username,
            "rating": row.rating,
            "text": row.text,
            "created_at": row.created_at,
        }

    def list_for(self, product_id: int) -> list[dict]:
        with self.make_session() as session:
            rows = session.scalars(
                select(Review)
                .where(Review.product_id == product_id)
                .order_by(Review.created_at.desc(), Review.id.desc())
            )
            return [self._as_dict(row) for row in rows]

    def stats(self, product_ids: list[int]) -> dict[int, tuple[float, int]]:
        if not product_ids:
            return {}
        with self.make_session() as session:
            rows = session.execute(
                select(Review.product_id, func.sum(Review.rating), func.count(Review.id))
                .where(Review.product_id.in_(product_ids))
                .group_by(Review.product_id)
            )
            return {pid: (_average(float(total), count), count) for pid, total, count in rows}

    def exists(self, product_id: int, user_id: int) -> bool:
        with self.make_session() as session:
            found = session.scalar(
                select(Review.id).where(Review.product_id == product_id, Review.user_id == user_id)
            )
            return found is not None

    def add(self, review: dict) -> dict:
        with self.make_session() as session:
            row = Review(**{k: v for k, v in review.items() if k != "id"})
            session.add(row)
            try:
                session.commit()
            except IntegrityError as error:
                raise DuplicateReviewError from error
            return self._as_dict(row)

    def add_many(self, reviews: list[dict]) -> None:
        with self.make_session() as session:
            session.add_all(Review(**review) for review in reviews)
            session.commit()

    def clear(self) -> None:
        with self.make_session() as session:
            session.query(Review).delete()
            session.commit()

    def is_up(self) -> bool:
        try:
            with self.make_session() as session:
                session.scalar(select(func.count(Review.id)))
            return True
        except SQLAlchemyError:
            return False


class MongoReviews:
    def __init__(self, url: str, database: str) -> None:
        # tz_aware: times come back as UTC; short timeout: a stopped MongoDB shows as "down" fast.
        self.client = MongoClient(url, tz_aware=True, tzinfo=UTC, serverSelectionTimeoutMS=3000)
        self.collection = self.client[database]["reviews"]
        self.indexes_ready = False

    def _ensure_indexes(self) -> None:
        if not self.indexes_ready:
            self.collection.create_index(
                [("product_id", ASCENDING), ("user_id", ASCENDING)], unique=True
            )
            self.collection.create_index([("product_id", ASCENDING), ("created_at", DESCENDING)])
            self.indexes_ready = True

    @staticmethod
    def _as_dict(document: dict) -> dict:
        review = {key: value for key, value in document.items() if key != "_id"}
        review["id"] = str(document["_id"])
        return review

    def list_for(self, product_id: int) -> list[dict]:
        cursor = self.collection.find({"product_id": product_id}).sort(
            [("created_at", DESCENDING), ("_id", DESCENDING)]
        )
        return [self._as_dict(document) for document in cursor]

    def stats(self, product_ids: list[int]) -> dict[int, tuple[float, int]]:
        if not product_ids:
            return {}
        pipeline = [
            {"$match": {"product_id": {"$in": product_ids}}},
            {"$group": {"_id": "$product_id", "total": {"$sum": "$rating"}, "count": {"$sum": 1}}},
        ]
        return {
            row["_id"]: (_average(row["total"], row["count"]), row["count"])
            for row in self.collection.aggregate(pipeline)
        }

    def exists(self, product_id: int, user_id: int) -> bool:
        return (
            self.collection.count_documents({"product_id": product_id, "user_id": user_id}, limit=1)
            > 0
        )

    def add(self, review: dict) -> dict:
        self._ensure_indexes()
        document = {key: value for key, value in review.items() if key != "id"}
        try:
            result = self.collection.insert_one(document)
        except DuplicateKeyError as error:
            raise DuplicateReviewError from error
        return self._as_dict({**document, "_id": result.inserted_id})

    def add_many(self, reviews: list[dict]) -> None:
        self._ensure_indexes()
        if reviews:
            self.collection.insert_many([dict(review) for review in reviews])

    def clear(self) -> None:
        self.collection.delete_many({})
        self._ensure_indexes()

    def is_up(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except PyMongoError:
            return False

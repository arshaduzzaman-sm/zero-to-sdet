"""Categories, products (search, filter, sort, pages) and reviews."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Query, Response
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..deps import (
    AdminUser,
    AppClock,
    CurrentUser,
    Db,
    MaybeUser,
    PageNumber,
    PageSize,
    Reviews,
    page_count,
)
from ..errors import ApiError, not_found
from ..models import Category, Order, OrderItem, Product, User
from ..reviews import DuplicateReviewError
from ..schemas import (
    CategoryOut,
    Page,
    ProductIn,
    ProductOut,
    ProductUpdateIn,
    ReviewIn,
    ReviewOut,
)

router = APIRouter(tags=["Catalog"])

BOUGHT = ("paid", "shipped", "delivered")
SEARCH_HELP = "Text in the name or description"
CATEGORY_HELP = "Category slug, e.g. testing-books"
STOCK_HELP = "true: only products you can buy now; false: only sold-out ones"


class Sort(StrEnum):
    newest = "newest"
    price = "price"
    price_desc = "-price"
    name = "name"
    name_desc = "-name"


ORDER_BY = {
    Sort.newest: (Product.created_at.desc(), Product.id.desc()),
    Sort.price: (Product.price_cents.asc(), Product.id.asc()),
    Sort.price_desc: (Product.price_cents.desc(), Product.id.asc()),
    Sort.name: (Product.name.asc(), Product.id.asc()),
    Sort.name_desc: (Product.name.desc(), Product.id.asc()),
}


def product_out(product: Product, stats: dict[int, tuple[float, int]]) -> ProductOut:
    average, count = stats.get(product.id, (None, 0))
    return ProductOut(
        id=product.id,
        sku=product.sku,
        name=product.name,
        description=product.description,
        category=CategoryOut.model_validate(product.category),
        price_cents=product.price_cents,
        stock=product.stock,
        in_stock=product.stock > 0,
        is_active=product.is_active,
        rating_average=average,
        rating_count=count,
        created_at=product.created_at,
    )


def visible_product(db: Session, product_id: int, user: User | None) -> Product:
    """Inactive products are hidden from everyone but admins."""
    product = db.get(Product, product_id)
    if product is None or (not product.is_active and (user is None or user.role != "admin")):
        raise not_found("product")
    return product


@router.get("/categories", response_model=list[CategoryOut], summary="List categories")
def list_categories(db: Db) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.name)))


@router.get("/products", response_model=Page[ProductOut], summary="Search and list products")
def list_products(
    db: Db,
    user: MaybeUser,
    reviews: Reviews,
    q: Annotated[str | None, Query(max_length=100, description=SEARCH_HELP)] = None,
    category: Annotated[str | None, Query(max_length=60, description=CATEGORY_HELP)] = None,
    min_price_cents: Annotated[int | None, Query(ge=0)] = None,
    max_price_cents: Annotated[int | None, Query(ge=0)] = None,
    in_stock: Annotated[bool | None, Query(description=STOCK_HELP)] = None,
    sort: Sort = Sort.newest,
    page: PageNumber = 1,
    size: PageSize = 20,
    include_inactive: Annotated[bool, Query(description="Admins only")] = False,
) -> dict:
    low, high = min_price_cents, max_price_cents
    if low is not None and high is not None and low > high:
        raise ApiError(
            400, "INVALID_PRICE_RANGE", "min_price_cents is bigger than max_price_cents."
        )
    query = select(Product)
    if not (include_inactive and user is not None and user.role == "admin"):
        query = query.where(Product.is_active.is_(True))
    if q and q.strip():
        text = q.strip().lower()
        query = query.where(
            or_(
                func.lower(Product.name).contains(text, autoescape=True),
                func.lower(Product.description).contains(text, autoescape=True),
            )
        )
    if category:
        query = query.join(Category).where(Category.slug == category)
    if min_price_cents is not None:
        query = query.where(Product.price_cents >= min_price_cents)
    if max_price_cents is not None:
        query = query.where(Product.price_cents <= max_price_cents)
    if in_stock is True:
        query = query.where(Product.stock > 0)
    elif in_stock is False:
        query = query.where(Product.stock == 0)
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    products = db.scalars(
        query.order_by(*ORDER_BY[sort]).offset((page - 1) * size).limit(size)
    ).all()
    stats = reviews.stats([p.id for p in products])
    return {
        "items": [product_out(p, stats) for p in products],
        "page": page,
        "size": size,
        "total": total,
        "pages": page_count(total, size),
    }


@router.get("/products/{product_id}", response_model=ProductOut, summary="Get one product")
def get_product(product_id: int, db: Db, user: MaybeUser, reviews: Reviews) -> ProductOut:
    product = visible_product(db, product_id, user)
    return product_out(product, reviews.stats([product.id]))


def check_category(db: Session, category_id: int) -> None:
    if db.get(Category, category_id) is None:
        raise ApiError(400, "CATEGORY_NOT_FOUND", f"There is no category with id {category_id}.")


@router.post(
    "/products", status_code=201, response_model=ProductOut, summary="Add a product (admin)"
)
def create_product(body: ProductIn, _admin: AdminUser, db: Db, clock: AppClock) -> ProductOut:
    check_category(db, body.category_id)
    if db.scalars(select(Product).where(Product.sku == body.sku)).first():
        raise ApiError(409, "SKU_TAKEN", f"A product with SKU {body.sku} already exists.")
    product = Product(**body.model_dump(), created_at=clock.now())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product_out(product, {})


@router.patch(
    "/products/{product_id}", response_model=ProductOut, summary="Change a product (admin)"
)
def update_product(
    product_id: int, body: ProductUpdateIn, _admin: AdminUser, db: Db, reviews: Reviews
) -> ProductOut:
    product = db.get(Product, product_id)
    if product is None:
        raise not_found("product")
    changes = body.model_dump(exclude_unset=True, exclude_none=True)
    if "category_id" in changes:
        check_category(db, changes["category_id"])
    for name, value in changes.items():
        setattr(product, name, value)
    db.commit()
    db.refresh(product)
    return product_out(product, reviews.stats([product.id]))


@router.delete(
    "/products/{product_id}", status_code=204, summary="Hide a product from customers (admin)"
)
def delete_product(product_id: int, _admin: AdminUser, db: Db) -> Response:
    """A soft delete: the product stays in old orders but customers cannot see or buy it."""
    product = db.get(Product, product_id)
    if product is None:
        raise not_found("product")
    product.is_active = False
    db.commit()
    return Response(status_code=204)


@router.get(
    "/products/{product_id}/reviews", response_model=list[ReviewOut], summary="Read reviews"
)
def list_reviews(product_id: int, db: Db, user: MaybeUser, reviews: Reviews) -> list[dict]:
    visible_product(db, product_id, user)
    return reviews.list_for(product_id)


@router.post(
    "/products/{product_id}/reviews",
    status_code=201,
    response_model=ReviewOut,
    summary="Review a product you bought",
)
def create_review(
    product_id: int, body: ReviewIn, user: CurrentUser, db: Db, clock: AppClock, reviews: Reviews
) -> dict:
    visible_product(db, product_id, user)
    bought = db.scalar(
        select(func.count(OrderItem.order_id))
        .join(Order)
        .where(
            Order.user_id == user.id,
            Order.status.in_(BOUGHT),
            OrderItem.product_id == product_id,
        )
    )
    if not bought:
        raise ApiError(403, "NOT_A_BUYER", "You can review only products you have bought.")
    already = ApiError(409, "ALREADY_REVIEWED", "You have already reviewed this product.")
    if reviews.exists(product_id, user.id):
        raise already
    try:
        return reviews.add(
            {
                "product_id": product_id,
                "user_id": user.id,
                "username": user.username,
                "rating": body.rating,
                "text": body.text,
                "created_at": clock.now(),
            }
        )
    except DuplicateReviewError:  # two requests at the same moment
        raise already from None

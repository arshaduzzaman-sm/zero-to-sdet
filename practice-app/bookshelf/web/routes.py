"""The web pages. Each one calls the same function as its API endpoint, so the
web page and the API always follow the same rules."""

from __future__ import annotations

from urllib.parse import quote, urlencode

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from ..api import admin as admin_api
from ..api import auth as auth_api
from ..api import cart as cart_api
from ..api import orders as orders_api
from ..api import products as products_api
from ..api import tools as tools_api
from ..api import users as users_api
from ..deps import AppClock, AppOutbox, AppSettings, Db, Hasher, Reviews
from ..errors import ApiError
from ..schemas import (
    CartItemIn,
    CheckoutIn,
    CouponIn,
    EmailIn,
    LoginIn,
    OrderStatusIn,
    ProductIn,
    ProductUpdateIn,
    QuantityIn,
    ResetPasswordIn,
    ReviewIn,
    SignupIn,
    UserUpdateIn,
    VerifyIn,
)
from .helpers import (
    CHOOSE_PICTURE,
    SESSION_COOKIE,
    Form,
    WebUser,
    chosen_file,
    go,
    need_admin,
    need_user,
    parse,
    parse_money,
    render,
    safe_next,
    secure_cookies,
)

router = APIRouter(include_in_schema=False)

SORTS = [
    ("newest", "Newest first"),
    ("price", "Price: low to high"),
    ("-price", "Price: high to low"),
    ("name", "Name: A to Z"),
    ("-name", "Name: Z to A"),
]
PAGE_SIZE = 12


# ----- Catalog -----


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Db, user: WebUser, reviews: Reviews) -> Response:
    query = request.query_params
    errors: dict[str, str] = {}
    prices = {}
    for field in ("min_price", "max_price"):
        try:
            prices[field] = parse_money(query.get(field, ""))
        except ValueError as error:
            errors[field] = str(error)
            prices[field] = None
    sort = query.get("sort", "newest")
    if sort not in dict(SORTS):
        sort = "newest"
    try:
        page = max(1, int(query.get("page", "1")))
    except ValueError:
        page = 1
    filters = {
        "q": query.get("q", "").strip()[:100] or None,
        "category": query.get("category") or None,
        "min_price_cents": prices["min_price"],
        "max_price_cents": prices["max_price"],
    }
    try:
        result = products_api.list_products(
            db=db,
            user=user,
            reviews=reviews,
            sort=sort,
            page=page,
            size=PAGE_SIZE,
            in_stock=None,
            include_inactive=False,
            **filters,
        )
    except ApiError as error:
        errors["max_price"] = error.message
        filters["min_price_cents"] = filters["max_price_cents"] = None
        result = products_api.list_products(
            db=db,
            user=user,
            reviews=reviews,
            sort=sort,
            page=page,
            size=PAGE_SIZE,
            in_stock=None,
            include_inactive=False,
            **filters,
        )
    kept = {key: value for key, value in query.items() if key not in ("page", "msg")}
    page_links = [(n, "/?" + urlencode({**kept, "page": n})) for n in range(1, result["pages"] + 1)]
    return render(
        request,
        "home.html",
        {
            "result": result,
            "page_links": page_links,
            "categories": products_api.list_categories(db=db),
            "sorts": SORTS,
            "form": {**query, "sort": sort},
            "errors": errors,
        },
        user=user,
    )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_page(
    product_id: int, request: Request, db: Db, user: WebUser, reviews: Reviews
) -> Response:
    product = products_api.get_product(product_id=product_id, db=db, user=user, reviews=reviews)
    return render(
        request,
        "product.html",
        {
            "product": product,
            "reviews": products_api.list_reviews(
                product_id=product_id, db=db, user=user, reviews=reviews
            ),
            "errors": {},
            "form": {},
        },
        user=user,
    )


@router.get("/products/{product_id}/image")
def product_image(product_id: int, db: Db, user: WebUser, settings: AppSettings) -> Response:
    """Same as GET /api/products/{id}/image, but knows the logged-in admin (cookie),
    so the admin page can show images of hidden products too."""
    return products_api.product_image(product_id=product_id, db=db, user=user, settings=settings)


@router.post("/products/{product_id}/reviews")
def add_review(
    product_id: int,
    request: Request,
    form: Form,
    db: Db,
    user: WebUser,
    clock: AppClock,
    reviews: Reviews,
) -> Response:
    user = need_user(request, user)
    body, errors = parse(ReviewIn, form)
    if body is not None:
        try:
            products_api.create_review(
                product_id=product_id, body=body, user=user, db=db, clock=clock, reviews=reviews
            )
            return go(f"/products/{product_id}", "reviewed")
        except ApiError as error:
            errors["form"] = error.message
    product = products_api.get_product(product_id=product_id, db=db, user=user, reviews=reviews)
    return render(
        request,
        "product.html",
        {
            "product": product,
            "reviews": reviews.list_for(product_id),
            "errors": errors,
            "form": form,
        },
        status=400,
        user=user,
    )


# ----- Accounts -----


def set_login(response: Response, request: Request, token: str, minutes: int) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=minutes * 60,
        httponly=True,  # page scripts cannot read it
        samesite="lax",  # other sites cannot send it with their forms
        secure=secure_cookies(request),
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: WebUser) -> Response:
    return render(
        request,
        "login.html",
        {"form": {}, "errors": {}, "next": safe_next(request.query_params.get("next"))},
        user=user,
    )


@router.post("/login")
def login(
    request: Request, form: Form, db: Db, settings: AppSettings, clock: AppClock, hasher: Hasher
) -> Response:
    next_path = safe_next(form.get("next"))
    body, errors = parse(LoginIn, form)
    if body is not None:
        try:
            token = auth_api.login(body=body, db=db, settings=settings, clock=clock, hasher=hasher)
            response = go(next_path, "logged_in")
            set_login(response, request, token.access_token, settings.token_minutes)
            return response
        except ApiError as error:
            if error.code == "EMAIL_NOT_VERIFIED":
                user = auth_api.find_user(db, body.username)
                return go(f"/verify?email={quote(user.email)}" if user else "/verify")
            errors["form"] = error.message
    return render(
        request,
        "login.html",
        {"form": {"username": form.get("username", "")}, "errors": errors, "next": next_path},
        status=400,
    )


@router.post("/logout")
def logout(request: Request, form: Form) -> Response:
    response = go("/", "logged_out")
    response.delete_cookie(SESSION_COOKIE)
    return response


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, user: WebUser) -> Response:
    return render(request, "signup.html", {"form": {}, "errors": {}}, user=user)


@router.post("/signup")
def signup(
    request: Request,
    form: Form,
    db: Db,
    settings: AppSettings,
    clock: AppClock,
    outbox: AppOutbox,
    hasher: Hasher,
) -> Response:
    body, errors = parse(SignupIn, form)
    if body is not None:
        try:
            user = auth_api.signup(
                body=body, db=db, settings=settings, clock=clock, outbox=outbox, hasher=hasher
            )
            return go(f"/verify?email={quote(user.email)}", "signed_up")
        except ApiError as error:
            field = {"EMAIL_TAKEN": "email", "USERNAME_TAKEN": "username"}.get(error.code, "form")
            errors[field] = error.message
    kept = {key: value for key, value in form.items() if key != "password"}
    return render(request, "signup.html", {"form": kept, "errors": errors}, status=400)


@router.get("/verify", response_class=HTMLResponse)
def verify_page(request: Request, user: WebUser) -> Response:
    email = request.query_params.get("email", "")[:254]
    return render(request, "verify.html", {"form": {"email": email}, "errors": {}}, user=user)


@router.post("/verify")
def verify(
    request: Request, form: Form, db: Db, settings: AppSettings, clock: AppClock, outbox: AppOutbox
) -> Response:
    if form.get("action") == "resend":
        body, errors = parse(EmailIn, form)
        if body is not None:
            auth_api.resend_code(body=body, db=db, settings=settings, clock=clock, outbox=outbox)
            return go(f"/verify?email={quote(body.email)}", "code_sent")
    else:
        body, errors = parse(VerifyIn, form)
        if body is not None:
            try:
                auth_api.verify(body=body, db=db, settings=settings, clock=clock)
                return go("/login", "verified")
            except ApiError as error:
                errors["code"] = error.message
    return render(request, "verify.html", {"form": form, "errors": errors}, status=400)


@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_page(request: Request, user: WebUser) -> Response:
    return render(request, "forgot.html", {"form": {}, "errors": {}}, user=user)


@router.post("/forgot-password")
def forgot(
    request: Request, form: Form, db: Db, settings: AppSettings, clock: AppClock, outbox: AppOutbox
) -> Response:
    body, errors = parse(EmailIn, form)
    if body is not None:
        auth_api.forgot_password(body=body, db=db, settings=settings, clock=clock, outbox=outbox)
        return go(f"/reset-password?email={quote(body.email)}", "code_sent")
    return render(request, "forgot.html", {"form": form, "errors": errors}, status=400)


@router.get("/reset-password", response_class=HTMLResponse)
def reset_page(request: Request, user: WebUser) -> Response:
    email = request.query_params.get("email", "")[:254]
    return render(request, "reset.html", {"form": {"email": email}, "errors": {}}, user=user)


@router.post("/reset-password")
def reset_password(
    request: Request, form: Form, db: Db, settings: AppSettings, clock: AppClock, hasher: Hasher
) -> Response:
    body, errors = parse(ResetPasswordIn, form)
    if body is not None:
        try:
            auth_api.reset_password(body=body, db=db, settings=settings, clock=clock, hasher=hasher)
            return go("/login", "password_changed")
        except ApiError as error:
            errors["code"] = error.message
    kept = {"email": form.get("email", ""), "code": form.get("code", "")}
    return render(request, "reset.html", {"form": kept, "errors": errors}, status=400)


@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, user: WebUser) -> Response:
    user = need_user(request, user)
    form = {"full_name": user.full_name, "shipping_address": user.shipping_address or ""}
    return render(request, "profile.html", {"form": form, "errors": {}}, user=user)


@router.post("/profile")
def save_profile(request: Request, form: Form, db: Db, user: WebUser) -> Response:
    user = need_user(request, user)
    body, errors = parse(UserUpdateIn, form)
    if body is not None:
        users_api.update_profile(body=body, user=user, db=db)
        return go("/profile", "profile_saved")
    return render(request, "profile.html", {"form": form, "errors": errors}, status=400, user=user)


@router.get("/profile/avatar")
def my_avatar(request: Request, user: WebUser, settings: AppSettings) -> Response:
    user = need_user(request, user)
    return users_api.avatar_response(settings, user)


@router.post("/profile/avatar")
def save_avatar(
    request: Request, form: Form, db: Db, user: WebUser, settings: AppSettings, clock: AppClock
) -> Response:
    user = need_user(request, user)
    file = chosen_file(form)
    try:
        if file is None:
            raise ApiError(400, "NO_FILE", CHOOSE_PICTURE)
        users_api.upload_avatar(user=user, db=db, settings=settings, clock=clock, file=file)
        return go("/profile", "avatar_saved")
    except ApiError as error:
        db.rollback()
        form = {"full_name": user.full_name, "shipping_address": user.shipping_address or ""}
        errors = {"avatar": error.message}
        return render(
            request, "profile.html", {"form": form, "errors": errors}, status=400, user=user
        )


@router.post("/profile/avatar/delete")
def remove_avatar(
    request: Request, form: Form, db: Db, user: WebUser, settings: AppSettings
) -> Response:
    user = need_user(request, user)
    if user.avatar_path:
        users_api.delete_avatar(user=user, db=db, settings=settings)
    return go("/profile", "avatar_removed")


# ----- Cart and checkout -----


def cart_page_response(request, db, user, clock, errors=None, status=200, form=None):
    cart = cart_api.show_cart(user=user, db=db, clock=clock)
    return render(
        request,
        "cart.html",
        {"cart": cart, "errors": errors or {}, "form": form or {}, "cart_count": cart.item_count},
        status=status,
        user=user,
    )


@router.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request, db: Db, user: WebUser, clock: AppClock) -> Response:
    user = need_user(request, user)
    return cart_page_response(request, db, user, clock)


@router.post("/cart/items")
def add_to_cart(
    request: Request, form: Form, db: Db, user: WebUser, clock: AppClock, reviews: Reviews
) -> Response:
    user = need_user(request, user)
    body, errors = parse(
        CartItemIn, {"product_id": form.get("product_id"), "quantity": form.get("quantity") or 1}
    )
    if body is not None:
        try:
            cart_api.add_item(body=body, user=user, db=db, clock=clock)
            return go(f"/products/{body.product_id}", "added")
        except ApiError as error:
            errors["quantity"] = error.message
    product_id = int(form.get("product_id", "0") or 0)
    product = products_api.get_product(product_id=product_id, db=db, user=user, reviews=reviews)
    return render(
        request,
        "product.html",
        {
            "product": product,
            "reviews": reviews.list_for(product_id),
            "errors": errors,
            "form": form,
        },
        status=400,
        user=user,
    )


@router.post("/cart/items/{product_id}")
def update_cart_line(
    product_id: int, request: Request, form: Form, db: Db, user: WebUser, clock: AppClock
) -> Response:
    user = need_user(request, user)
    try:
        if form.get("action") == "remove":
            cart_api.remove_item(product_id=product_id, user=user, db=db, clock=clock)
            return go("/cart", "removed")
        body, errors = parse(QuantityIn, {"quantity": form.get("quantity")})
        if body is None:
            return cart_page_response(
                request, db, user, clock, {f"quantity-{product_id}": errors["quantity"]}, 400
            )
        cart_api.change_quantity(product_id=product_id, body=body, user=user, db=db, clock=clock)
        return go("/cart", "cart_updated")
    except ApiError as error:
        return cart_page_response(
            request, db, user, clock, {f"quantity-{product_id}": error.message}, 400
        )


@router.post("/cart/coupon")
def coupon(request: Request, form: Form, db: Db, user: WebUser, clock: AppClock) -> Response:
    user = need_user(request, user)
    if form.get("action") == "remove":
        cart_api.remove_coupon(user=user, db=db, clock=clock)
        return go("/cart", "coupon_removed")
    body, errors = parse(CouponIn, form)
    if body is not None:
        try:
            cart_api.apply_coupon(body=body, user=user, db=db, clock=clock)
            return go("/cart", "coupon_added")
        except ApiError as error:
            errors["code"] = error.message
    return cart_page_response(request, db, user, clock, errors, 400, form)


@router.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request, db: Db, user: WebUser, clock: AppClock) -> Response:
    user = need_user(request, user)
    cart = cart_api.show_cart(user=user, db=db, clock=clock)
    if not cart.items:
        return go("/cart")
    form = {"shipping_address": user.shipping_address or ""}
    return render(request, "checkout.html", {"cart": cart, "form": form, "errors": {}}, user=user)


@router.post("/checkout")
def place_order(
    request: Request,
    form: Form,
    db: Db,
    user: WebUser,
    clock: AppClock,
    settings: AppSettings,
    outbox: AppOutbox,
) -> Response:
    user = need_user(request, user)
    body, errors = parse(CheckoutIn, form)
    if body is not None:
        try:
            order = orders_api.checkout(
                body=body, user=user, db=db, clock=clock, settings=settings, outbox=outbox
            )
            return go(f"/orders/{order.id}", "ordered")
        except ApiError as error:
            field = {
                "INVALID_CARD": "card_number",
                "CARD_EXPIRED": "expiry",
                "ADDRESS_REQUIRED": "shipping_address",
            }.get(error.code, "form")
            errors[field] = error.message
    cart = cart_api.show_cart(user=user, db=db, clock=clock)
    kept = {"shipping_address": form.get("shipping_address", "")}  # never echo card data back
    return render(
        request,
        "checkout.html",
        {"cart": cart, "form": kept, "errors": errors},
        status=400,
        user=user,
    )


# ----- Orders -----


@router.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request, db: Db, user: WebUser) -> Response:
    user = need_user(request, user)
    orders = orders_api.list_orders(user=user, db=db, page=1, size=50)
    return render(request, "orders.html", {"orders": orders}, user=user)


@router.get("/orders/{order_id}", response_class=HTMLResponse)
def order_page(order_id: int, request: Request, db: Db, user: WebUser) -> Response:
    user = need_user(request, user)
    order = orders_api.get_order(order_id=order_id, user=user, db=db)
    return render(request, "order.html", {"order": order, "errors": {}}, user=user)


@router.get("/orders/{order_id}/invoice.pdf")
def order_invoice(order_id: int, request: Request, db: Db, user: WebUser) -> Response:
    user = need_user(request, user)
    return orders_api.order_invoice(order_id=order_id, user=user, db=db)


@router.post("/orders/{order_id}/cancel")
def cancel(
    order_id: int, request: Request, form: Form, db: Db, user: WebUser, clock: AppClock
) -> Response:
    user = need_user(request, user)
    try:
        orders_api.cancel_order(order_id=order_id, user=user, db=db, clock=clock)
        return go(f"/orders/{order_id}", "cancelled")
    except ApiError as error:
        order = orders_api.get_order(order_id=order_id, user=user, db=db)
        return render(
            request,
            "order.html",
            {"order": order, "errors": {"form": error.message}},
            status=409,
            user=user,
        )


# ----- Status -----


@router.get("/status", response_class=HTMLResponse)
def status_page(request: Request, user: WebUser, settings: AppSettings) -> Response:
    report = tools_api.health_report(request.app)
    kinds = settings.database_kinds
    email = "Email (Mailpit)" if settings.smtp_host else "Email"
    email_job = (
        "Catches every email: sign-up codes, reset codes, order confirmations"
        if settings.smtp_host
        else "Emails are printed in the terminal and saved in data/outbox/"
    )
    parts = [
        ("api", "Web shop and API", "The pages you see and the REST API"),
        ("main_database", f"Main database ({kinds['main']})", "Users, products, carts, orders"),
        (
            "reporting_database",
            f"Reporting copy ({kinds['reporting']})",
            "Order totals for reports",
        ),
        ("reviews_database", f"Reviews ({kinds['reviews']})", "Product reviews"),
        ("email", email, email_job),
    ]
    status = 200 if report["status"] == "ok" else 503
    return render(
        request, "status.html", {"report": report, "parts": parts}, status=status, user=user
    )


# ----- Admin -----


def admin_page_response(request, db, user, reviews, errors=None, status=200, form=None):
    products = products_api.list_products(
        db=db,
        user=user,
        reviews=reviews,
        q=None,
        category=None,
        min_price_cents=None,
        max_price_cents=None,
        in_stock=None,
        sort="name",
        page=1,
        size=50,
        include_inactive=True,
    )
    orders = admin_api.all_orders(_admin=user, db=db, status=None, page=1, size=20)
    return render(
        request,
        "admin.html",
        {
            "products": products,
            "orders": orders,
            "errors": errors or {},
            "form": form or {},
            "categories": products_api.list_categories(db=db),
            "next_status": admin_api.NEXT_STATUS,
        },
        status=status,
        user=user,
    )


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Db, user: WebUser, reviews: Reviews) -> Response:
    user = need_admin(request, user)
    return admin_page_response(request, db, user, reviews)


@router.post("/admin/products")
def admin_new_product(
    request: Request, form: Form, db: Db, user: WebUser, clock: AppClock, reviews: Reviews
) -> Response:
    user = need_admin(request, user)
    data = dict(form)
    errors: dict[str, str] = {}
    try:
        data["price_cents"] = parse_money(form.get("price", "")) or 0
    except ValueError as error:
        errors["price"] = str(error)
    data["is_active"] = True
    body, more = parse(ProductIn, data)
    errors.update({("price" if k == "price_cents" else k): v for k, v in more.items()})
    if body is not None and not errors:
        try:
            products_api.create_product(body=body, _admin=user, db=db, clock=clock)
            return go("/admin", "product_created")
        except ApiError as error:
            errors["sku"] = error.message
    return admin_page_response(request, db, user, reviews, errors, 400, form)


@router.post("/admin/products/{product_id}")
def admin_save_product(
    product_id: int, request: Request, form: Form, db: Db, user: WebUser, reviews: Reviews
) -> Response:
    user = need_admin(request, user)
    body, errors = parse(
        ProductUpdateIn, {"stock": form.get("stock"), "is_active": form.get("is_active") == "on"}
    )
    if body is not None:
        products_api.update_product(
            product_id=product_id, body=body, _admin=user, db=db, reviews=reviews
        )
        return go("/admin", "product_saved")
    return admin_page_response(
        request, db, user, reviews, {f"stock-{product_id}": errors.get("stock", "Not valid.")}, 400
    )


@router.post("/admin/products/{product_id}/image")
def admin_product_image(
    product_id: int,
    request: Request,
    form: Form,
    db: Db,
    user: WebUser,
    settings: AppSettings,
    clock: AppClock,
    reviews: Reviews,
) -> Response:
    user = need_admin(request, user)
    file = chosen_file(form)
    try:
        if file is None:
            raise ApiError(400, "NO_FILE", CHOOSE_PICTURE)
        products_api.upload_product_image(
            product_id=product_id,
            admin=user,
            db=db,
            settings=settings,
            clock=clock,
            reviews=reviews,
            file=file,
        )
        return go("/admin", "image_saved")
    except ApiError as error:
        db.rollback()
        errors = {f"image-{product_id}": error.message}
        return admin_page_response(request, db, user, reviews, errors, 400)


@router.post("/admin/orders/{order_id}")
def admin_order_status(
    order_id: int,
    request: Request,
    form: Form,
    db: Db,
    user: WebUser,
    clock: AppClock,
    reviews: Reviews,
) -> Response:
    user = need_admin(request, user)
    body, errors = parse(OrderStatusIn, form)
    if body is not None:
        try:
            admin_api.change_status(order_id=order_id, body=body, _admin=user, db=db, clock=clock)
            return go("/admin", "status_changed")
        except ApiError as error:
            errors["status"] = error.message
    return admin_page_response(
        request, db, user, reviews, {f"order-{order_id}": errors.get("status", "Not valid.")}, 400
    )


@router.post("/admin/reset")
def admin_reset(request: Request, form: Form, db: Db, user: WebUser, clock: AppClock) -> Response:
    user = need_admin(request, user)
    admin_api.reset(_admin=user, db=db, request=request, clock=clock)
    return go("/admin", "reset_done")


@router.post("/admin/reporting-sync")
def admin_sync(request: Request, form: Form, user: WebUser) -> Response:
    user = need_admin(request, user)
    admin_api.reporting_sync(_admin=user, request=request)
    return go("/admin", "synced")


def login_redirect(next_path: str, expired: bool) -> RedirectResponse:
    response = RedirectResponse(
        f"/login?next={quote(next_path)}&msg={'session_expired' if expired else 'login_needed'}",
        status_code=303,
    )
    if expired:
        response.delete_cookie(SESSION_COOKIE)
    return response

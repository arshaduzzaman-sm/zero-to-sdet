"""Invoice PDFs, made on request from the order (nothing is stored).

The PDF uses the built-in Helvetica font, so it only holds Latin-1 text: any
other character (for example in a fake customer's name) becomes "?".
"""

from __future__ import annotations

from fpdf import FPDF

from .models import Order

NOTE = "Practice invoice from the Bookshelf practice app. Not a real document."


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    return f"{sign}${abs(cents) / 100:,.2f}"


def latin(text: str) -> str:
    return text.encode("latin-1", "replace").decode("latin-1")


def build_invoice(order: Order) -> bytes:
    pdf = FPDF(format="A4")
    pdf.set_title(f"Bookshelf invoice {order.id}")
    pdf.set_author("Bookshelf practice app")
    pdf.set_creation_date(order.created_at)
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=20)
    width = pdf.epw

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(width, 10, "Bookshelf", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(width, 5, NOTE, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(width, 8, f"Invoice for order #{order.id}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    details = [
        ("Date", order.created_at.strftime("%d %B %Y")),
        ("Status", order.status.capitalize()),
        ("Customer", f"{order.user.full_name} ({order.user.email})"),
        ("Ship to", order.shipping_address),
    ]
    for label, value in details:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(30, 6, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(width - 30, 6, latin(value), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    columns = (("Item", width - 75), ("Qty", 15), ("Price", 30), ("Total", 30))
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(235, 240, 248)
    for name, size in columns:
        pdf.cell(size, 8, name, border="B", fill=True, align="L" if name == "Item" else "R")
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    for item in order.items:
        name = latin(item.product.name)
        while pdf.get_string_width(name) > columns[0][1] - 2 and len(name) > 4:
            name = name[:-4] + "..."
        pdf.cell(columns[0][1], 7, name)
        pdf.cell(15, 7, str(item.quantity), align="R")
        pdf.cell(30, 7, money(item.unit_price_cents), align="R")
        pdf.cell(30, 7, money(item.unit_price_cents * item.quantity), align="R")
        pdf.ln()
    pdf.ln(3)

    discount = f"Discount ({order.coupon_code})" if order.coupon_code else "Discount"
    totals = [("Subtotal", order.subtotal_cents)]
    if order.discount_cents:
        totals.append((discount, -order.discount_cents))
    totals += [("Tax", order.tax_cents), ("Shipping", order.shipping_cents)]
    for label, cents in totals:
        pdf.cell(width - 30, 6, latin(label), align="R")
        pdf.cell(30, 6, money(cents), align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(width - 30, 8, "Total", align="R")
    pdf.cell(30, 8, money(order.total_cents), align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10)
    for payment in order.payments:
        line = (
            f"Payment {payment.sandbox_ref}: sandbox card ending {payment.card_last4}, "
            f"{money(payment.amount_cents)}, {payment.status}"
        )
        pdf.multi_cell(width, 6, latin(line), new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())

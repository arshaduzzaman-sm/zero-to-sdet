# Bug Hunt answers (spoilers)

> [!CAUTION]
> Stop here if you are still hunting. Each answer is easier to remember when you
> found the bug yourself first.

The Practice App has bugs planted on purpose. This is the starter set. More are
added with the topics that use them. Every bug is on by default; start the app
with `PRACTICE_APP_BUGS=off` to see the correct behavior.

| Code | Area | Short name |
| --- | --- | --- |
| BH-01 | Business rule (API and web) | Free shipping at exactly $50.00 |
| BH-02 | API | Page count is one short |
| BH-03 | Database (reporting copy) | Cancelled orders count as sales |
| BH-04 | Security (access control) | Anyone's invoice |
| BH-05 | Web page | The cart badge counts lines, not items |
| BH-06 | Security (time) | An old reset code still works |

---

## BH-01: Free shipping at exactly $50.00

- **Rule:** shipping is free when the order (after the discount) is **$50.00 or more**.
- **Steps:** every seed price ends in .99, so first make your own test data: log
  in as `admin` and add a product that costs $25.00 (admin page, or `POST /api/products`).
  Then log in as `arshad`, add 2 of it to the cart, and open the cart.
- **Expected:** shipping $0.00 at exactly $50.00.
- **Actual:** shipping $4.99. Free shipping only starts at $50.01.
- **Technique:** boundary value analysis. Test just below, at, and just above a limit.
- **Severity:** medium. Customers pay for shipping they should get free.

## BH-02: Page count is one short

- **Steps:** `GET /api/products?size=5`.
- **Expected:** `total` 12 and `pages` 3 (5 + 5 + 2).
- **Actual:** `pages` is 2. The last, partly filled page is not counted. Page 3
  still works if you ask for it, so a test that follows `pages` misses products.
  On the web shop the same mistake hides the last page link once there are more
  products than fit on one page.
- **Technique:** boundary values for pagination (a total that is not a multiple
  of the page size).
- **Severity:** medium. Products become hard to find.

## BH-03: Cancelled orders count as sales

- **Steps:** place an order, cancel it, then run the reporting sync
  (`POST /api/admin/reporting/sync` as admin). Compare `daily_sales` in the
  reporting database with the paid orders in the main database.
- **Expected:** `daily_sales.revenue_cents` counts only paid, shipped and delivered orders.
- **Actual:** cancelled orders are added to the revenue and the order count.
- **Technique:** compare the same data in two databases (multi-database testing).
- **Severity:** high. Reports show money the shop never kept.

## BH-04: Anyone's invoice

- **Steps:** log in as `arshad` and call `GET /api/orders/2/invoice.pdf`. Order 2
  belongs to `maria`.
- **Expected:** 404 `ORDER_NOT_FOUND`, the same as `GET /api/orders/2`.
- **Actual:** 200 with Maria's invoice: her name, email, address and what she bought.
- **Technique:** access control testing (change the id in the address; this is
  called IDOR, insecure direct object reference). Check every endpoint, not just one.
- **Severity:** critical. Personal data leaks to other customers.

## BH-05: The cart badge counts lines, not items

- **Steps:** log in on the web shop. Add 3 of the same book to the cart. Go back
  to the shop page.
- **Expected:** the cart badge in the header says 3, like the cart page and
  `item_count` in `GET /api/cart`.
- **Actual:** the badge says 1 (one line) on every page except the cart page.
- **Technique:** compare the same number in two places (web against API).
- **Severity:** low. Confusing, but the cart itself is right.

## BH-06: An old reset code still works

- **Rule:** a password reset code works for 10 minutes.
- **Steps:** ask for a reset code (`POST /api/auth/forgot-password`). As admin,
  move the clock 11 minutes ahead (`POST /api/admin/clock`). Use the code
  (`POST /api/auth/reset-password`).
- **Expected:** 400 `CODE_EXPIRED`. (The sign-up code does expire correctly.)
- **Actual:** the password changes.
- **Technique:** time-based testing with a controllable clock; compare two flows
  that should follow the same rule.
- **Severity:** high. An old code from a leaked email can still take over the account.

-- Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS orders
FROM orders GROUP BY month ORDER BY month

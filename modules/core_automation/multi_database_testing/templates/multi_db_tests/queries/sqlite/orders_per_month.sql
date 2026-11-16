-- Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS orders
FROM orders GROUP BY month ORDER BY month

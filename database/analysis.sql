
-- 1. Total sales records
SELECT COUNT(*) AS total_records
FROM sales;

-- 2. Total revenue
SELECT ROUND(SUM(quantity * price), 2) AS total_revenue
FROM sales;

-- 3. Total units sold
SELECT SUM(quantity) AS total_units_sold
FROM sales;

-- 4. Unique products
SELECT COUNT(DISTINCT stock_code) AS unique_products
FROM sales;

-- 5. Unique customers
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM sales;

-- 6. Top 10 countries by revenue
SELECT
    country,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;

-- 7. Monthly sales trend
SELECT
    strftime('%Y-%m', invoice_date) AS month,
    ROUND(SUM(quantity * price), 2) AS monthly_revenue,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY month
ORDER BY month;

-- 8. Top 10 products by revenue
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 10;

-- 9. Top 10 customers by revenue
SELECT
    customer_id,
    COUNT(DISTINCT invoice) AS total_orders,
    SUM(quantity) AS total_units,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;

-- 10. Top 10 products by units sold
SELECT
    stock_code,
    description,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
WHERE stock_code NOT IN ('M', 'DOT', 'POST')
GROUP BY stock_code, description
ORDER BY total_units_sold DESC
LIMIT 10;

-- 11. Average monthly demand by product
SELECT
    stock_code,
    description,
    SUM(quantity) AS total_units,
    COUNT(DISTINCT strftime('%Y-%m', invoice_date)) AS active_months,
    ROUND(
        1.0 * SUM(quantity) /
        COUNT(DISTINCT strftime('%Y-%m', invoice_date)), 2
    ) AS average_monthly_units
FROM sales
WHERE stock_code NOT IN ('M', 'DOT', 'POST')
GROUP BY stock_code, description
HAVING active_months >= 6
ORDER BY average_monthly_units DESC
LIMIT 10;

-- 12. Find duplicate product descriptions
SELECT
    stock_code,
    COUNT(DISTINCT description) AS description_count,
    GROUP_CONCAT(DISTINCT description) AS descriptions
FROM sales
GROUP BY stock_code
HAVING COUNT(DISTINCT description) > 1
ORDER BY description_count DESC
LIMIT 20;


-- 13. Top 10 products by revenue (excluding non-merchandise)
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
WHERE stock_code NOT IN ('M', 'DOT', 'POST')
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 10;


-- 14. Average selling price by product
SELECT
    stock_code,
    description,
    ROUND(AVG(price), 2) AS average_price,
    SUM(quantity) AS units_sold
FROM sales
WHERE stock_code NOT IN ('M', 'DOT', 'POST')
GROUP BY stock_code, description
HAVING SUM(quantity) > 100
ORDER BY average_price DESC
LIMIT 10;


-- 15. Customer purchasing frequency
SELECT
    CASE
        WHEN orders = 1 THEN 'One-time customer'
        WHEN orders BETWEEN 2 AND 5 THEN 'Occasional customer'
        WHEN orders BETWEEN 6 AND 15 THEN 'Regular customer'
        ELSE 'Frequent customer'
    END AS customer_segment,
    COUNT(*) AS customer_count
FROM (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice) AS orders
    FROM sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
)
GROUP BY customer_segment
ORDER BY customer_count DESC;


-- 16. Top 20 customers by lifetime sales value
SELECT
    customer_id,
    COUNT(DISTINCT invoice) AS total_orders,
    ROUND(SUM(quantity * price), 2) AS lifetime_revenue,
    ROUND(
        SUM(quantity * price) /
        COUNT(DISTINCT invoice), 2
    ) AS average_order_value
FROM sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY lifetime_revenue DESC
LIMIT 20;


-- 17. Yearly sales comparison
SELECT
    strftime('%Y', invoice_date) AS sales_year,
    COUNT(DISTINCT invoice) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY sales_year
ORDER BY sales_year;

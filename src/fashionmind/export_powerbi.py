
from pathlib import Path
import sqlite3
import csv

# Project paths
ROOT = Path(__file__).resolve().parents[2]

DB_PATH = ROOT / "database" / "fashionmind.db"
OUTPUT_DIR = ROOT / "data" / "processed" / "powerbi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Check database
if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

queries = {
    "kpi_summary": """
        SELECT
            COUNT(*) AS total_records,
            ROUND(SUM(quantity * price), 2) AS gross_sales_value,
            SUM(quantity) AS units_sold,
            COUNT(DISTINCT stock_code) AS unique_products,
            COUNT(DISTINCT customer_id) AS identified_customers
        FROM sales;
    """,

    "monthly_sales": """
        SELECT
            strftime('%Y-%m', invoice_date) AS month,
            COUNT(DISTINCT invoice) AS total_invoices,
            SUM(quantity) AS units_sold,
            ROUND(SUM(quantity * price), 2) AS revenue
        FROM sales
        GROUP BY month
        ORDER BY month;
    """,

    "country_sales": """
        SELECT
            country,
            COUNT(DISTINCT invoice) AS total_invoices,
            SUM(quantity) AS units_sold,
            ROUND(SUM(quantity * price), 2) AS revenue
        FROM sales
        GROUP BY country
        ORDER BY revenue DESC;
    """,

    "product_performance": """
        SELECT
            stock_code,
            description,
            SUM(quantity) AS units_sold,
            COUNT(DISTINCT invoice) AS total_invoices,
            ROUND(SUM(quantity * price), 2) AS revenue,
            ROUND(
                SUM(quantity * price) * 1.0 / NULLIF(SUM(quantity), 0),
                2
            ) AS weighted_average_selling_price
        FROM sales
        GROUP BY stock_code, description
        ORDER BY revenue DESC;
    """,

    "customer_performance": """
        SELECT
            customer_id,
            COUNT(DISTINCT invoice) AS invoice_count,
            SUM(quantity) AS units_purchased,
            ROUND(SUM(quantity * price), 2) AS historical_revenue,
            CASE
                WHEN COUNT(DISTINCT invoice) = 1 THEN 'One-time'
                WHEN COUNT(DISTINCT invoice) BETWEEN 2 AND 5 THEN 'Occasional'
                WHEN COUNT(DISTINCT invoice) BETWEEN 6 AND 15 THEN 'Regular'
                ELSE 'Frequent'
            END AS customer_segment
        FROM sales
        WHERE customer_id IS NOT NULL
        GROUP BY customer_id
        ORDER BY historical_revenue DESC;
    """,

    "customer_segment_summary": """
        WITH customers AS (
            SELECT
                customer_id,
                COUNT(DISTINCT invoice) AS invoice_count,
                SUM(quantity * price) AS revenue
            FROM sales
            WHERE customer_id IS NOT NULL
            GROUP BY customer_id
        ),
        segmented AS (
            SELECT
                CASE
                    WHEN invoice_count = 1 THEN 'One-time'
                    WHEN invoice_count BETWEEN 2 AND 5 THEN 'Occasional'
                    WHEN invoice_count BETWEEN 6 AND 15 THEN 'Regular'
                    ELSE 'Frequent'
                END AS customer_segment,
                revenue,
                invoice_count
            FROM customers
        )
        SELECT
            customer_segment,
            COUNT(*) AS customer_count,
            SUM(invoice_count) AS total_invoices,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS average_customer_revenue
        FROM segmented
        GROUP BY customer_segment
        ORDER BY customer_count DESC;
    """
}


def export_query(connection, filename, query):
    cursor = connection.execute(query)

    headers = [column[0] for column in cursor.description]
    output_file = OUTPUT_DIR / f"{filename}.csv"

    row_count = 0

    with output_file.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for row in cursor:
            writer.writerow(row)
            row_count += 1

    print(f"Exported: {filename}.csv | Rows: {row_count}")


def main():
    print("\nFASHIONMIND POWER BI DATA EXPORT")
    print("--------------------------------")

    with sqlite3.connect(DB_PATH) as connection:
        for filename, query in queries.items():
            export_query(connection, filename, query)

    print("\nEXPORT COMPLETED SUCCESSFULLY!")
    print(f"Files saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

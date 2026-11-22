
import csv
import sqlite3
from pathlib import Path

database_path = "database/fashionmind.db"
schema_path = "database/schema.sql"
csv_path = "data/processed/cleaned_sales.csv"

# Connect to SQLite
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Create database tables
with open(schema_path, "r", encoding="utf-8") as file:
    cursor.executescript(file.read())

# Clear previous imported records if rerunning
cursor.execute("DELETE FROM sales")

# Import cleaned sales data
insert_query = """
INSERT INTO sales (
    invoice, stock_code, description, quantity,
    invoice_date, price, customer_id, country
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

batch = []
total_records = 0

with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        batch.append((
            row["Invoice"],
            row["StockCode"],
            row["Description"],
            int(row["Quantity"]),
            row["InvoiceDate"],
            float(row["Price"]),
            row["Customer ID"] or None,
            row["Country"]
        ))

        if len(batch) == 10000:
            cursor.executemany(insert_query, batch)
            total_records += len(batch)
            batch.clear()

            if total_records % 100000 == 0:
                print("Imported:", total_records)

    if batch:
        cursor.executemany(insert_query, batch)
        total_records += len(batch)

connection.commit()

# Verify database records
cursor.execute("SELECT COUNT(*) FROM sales")
database_count = cursor.fetchone()[0]

connection.close()

print("\nFASHIONMIND DATABASE IMPORT COMPLETE")
print("------------------------------------")
print("Imported records:", total_records)
print("Database records:", database_count)
print("Database location:", database_path)

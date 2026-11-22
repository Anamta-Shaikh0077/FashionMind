
import csv
from pathlib import Path
from openpyxl import load_workbook

input_file = "data/raw/online_retail_II.xlsx"

output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

sales_file = output_folder / "cleaned_sales.csv"
review_file = output_folder / "records_for_review.csv"

headers = [
    "Invoice", "StockCode", "Description", "Quantity",
    "InvoiceDate", "Price", "Customer ID", "Country"
]

workbook = load_workbook(
    input_file,
    read_only=True,
    data_only=True
)

sales_count = 0
review_count = 0

with open(sales_file, "w", newline="", encoding="utf-8-sig") as sales_output, \
     open(review_file, "w", newline="", encoding="utf-8-sig") as review_output:

    sales_writer = csv.writer(sales_output)
    review_writer = csv.writer(review_output)

    sales_writer.writerow(headers)
    review_writer.writerow(headers + ["ReviewReason"])

    for sheet in workbook.worksheets:
        rows = sheet.iter_rows(values_only=True)
        next(rows)

        for row in rows:
            invoice, stock, description, quantity, date, price, customer, country = row

            reasons = []

            if str(invoice).startswith("C"):
                reasons.append("Cancelled invoice")

            if quantity is None or quantity <= 0:
                reasons.append("Non-positive or missing quantity")

            if price is None or price <= 0:
                reasons.append("Non-positive or missing price")

            if reasons:
                review_writer.writerow(
                    [str(value) if value is not None else "" for value in row]
                    + ["; ".join(reasons)]
                )
                review_count += 1

            else:
                sales_writer.writerow(
                    [str(value) if value is not None else "" for value in row]
                )
                sales_count += 1

workbook.close()

print("\nFASHIONMIND DATA CLEANING COMPLETE")
print("----------------------------------")
print("Valid sales records:", sales_count)
print("Records for review:", review_count)
print("Sales file:", sales_file)
print("Review file:", review_file)

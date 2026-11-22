
from openpyxl import load_workbook

file_path = "data/raw/online_retail_II.xlsx"

workbook = load_workbook(
    file_path,
    read_only=True,
    data_only=True
)

total_rows = 0
missing_customer = 0
missing_description = 0
negative_quantity = 0
invalid_price = 0
cancelled_invoices = 0

for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    next(rows)  # Skip column headings

    for row in rows:
        total_rows += 1

        invoice, stock, description, quantity, date, price, customer, country = row

        if customer is None:
            missing_customer += 1

        if description is None:
            missing_description += 1

        if quantity is not None and quantity < 0:
            negative_quantity += 1

        if price is not None and price <= 0:
            invalid_price += 1

        if str(invoice).startswith("C"):
            cancelled_invoices += 1

workbook.close()

print("\nFASHIONMIND - DATA QUALITY REPORT")
print("---------------------------------")
print("Total records:", total_rows)
print("Missing customer IDs:", missing_customer)
print("Missing descriptions:", missing_description)
print("Negative quantities:", negative_quantity)
print("Zero or negative prices:", invalid_price)
print("Cancelled invoices:", cancelled_invoices)

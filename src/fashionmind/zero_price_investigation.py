
from openpyxl import load_workbook

workbook = load_workbook(
    "data/raw/online_retail_II.xlsx",
    read_only=True,
    data_only=True
)

positive_quantity = 0
negative_quantity = 0
zero_quantity = 0
missing_customer = 0
identified_customer = 0

for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    next(rows)

    for row in rows:
        quantity = row[3]
        price = row[5]
        customer = row[6]

        if price == 0:
            if quantity is not None and quantity > 0:
                positive_quantity += 1
            elif quantity is not None and quantity < 0:
                negative_quantity += 1
            else:
                zero_quantity += 1

            if customer is None:
                missing_customer += 1
            else:
                identified_customer += 1

workbook.close()

print("ZERO-PRICE RECORD INVESTIGATION")
print("--------------------------------")
print("Positive quantities:", positive_quantity)
print("Negative quantities:", negative_quantity)
print("Zero or missing quantities:", zero_quantity)
print("Missing customer IDs:", missing_customer)
print("Identified customer IDs:", identified_customer)

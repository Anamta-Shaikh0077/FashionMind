
from openpyxl import load_workbook

file_path = "data/raw/online_retail_II.xlsx"

workbook = load_workbook(
    file_path,
    read_only=True,
    data_only=True
)

cancelled_and_negative = 0
cancelled_only = 0
negative_only = 0

samples = []

for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    next(rows)

    for row in rows:
        invoice, stock, description, quantity, date, price, customer, country = row

        is_cancelled = str(invoice).startswith("C")
        is_negative = quantity is not None and quantity < 0

        if is_cancelled and is_negative:
            cancelled_and_negative += 1
        elif is_cancelled:
            cancelled_only += 1
        elif is_negative:
            negative_only += 1

        if (is_cancelled or is_negative) and len(samples) < 10:
            samples.append(row)

workbook.close()

print("CANCELLED AND NEGATIVE:", cancelled_and_negative)
print("CANCELLED ONLY:", cancelled_only)
print("NEGATIVE ONLY:", negative_only)

print("\nSAMPLE RECORDS:")
for sample in samples:
    print(sample)

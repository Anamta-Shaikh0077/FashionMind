
from openpyxl import load_workbook

file_path = "data/raw/online_retail_II.xlsx"

workbook = load_workbook(
    file_path,
    read_only=True,
    data_only=True
)

zero_prices = 0
negative_prices = 0
samples = []

for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    next(rows)

    for row in rows:
        price = row[5]

        if price is not None and price == 0:
            zero_prices += 1

        elif price is not None and price < 0:
            negative_prices += 1

        if price is not None and price <= 0 and len(samples) < 15:
            samples.append(row)

workbook.close()

print("ZERO PRICES:", zero_prices)
print("NEGATIVE PRICES:", negative_prices)

print("\nSAMPLE RECORDS:")
for sample in samples:
    print(sample)

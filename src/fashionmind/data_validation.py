
import csv

files = {
    "Cleaned Sales": "data/processed/cleaned_sales.csv",
    "Records for Review": "data/processed/records_for_review.csv"
}

for name, path in files.items():
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        count = sum(1 for row in reader)

    print("\n", name)
    print("Columns:", len(header))
    print("Records:", count)
    print("Headers:", header)

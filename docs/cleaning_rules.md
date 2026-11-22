
# FashionMind - Data Cleaning Rules

## 1. Original Data
- Preserve the original Excel dataset.
- Never overwrite raw data.

## 2. Missing Values
- Missing Customer IDs: retain for general sales analysis.
- Missing Descriptions: flag for investigation.

## 3. Transaction Records
- Cancelled invoices: identify separately.
- Negative quantities: investigate as returns or adjustments.
- Do not combine cancellations with normal sales.

## 4. Price Validation
- Zero prices: flag and exclude from standard revenue calculations.
- Negative prices: investigate separately.
- Never silently replace invalid prices.

## 5. Data Integrity
- Keep a record of every cleaning operation.
- Document excluded records and reasons.
- Preserve original transaction values.

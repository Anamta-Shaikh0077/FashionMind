
# FashionMind — SQL Analysis Report

## 1. Project Overview

FashionMind is a Retail, Fashion and Supply Chain Intelligence Platform designed to turn retail transaction data into meaningful business insights.

This report documents the SQL analysis performed on the UCI Online Retail II dataset using SQLite.

**Main business question:**

How can a retail business use historical transaction data to understand sales performance, product demand and customer purchasing behaviour?

## 2. Dataset Information

- **Dataset:** Online Retail II
- **Source:** UCI Machine Learning Repository
- **Business context:** UK-based online retail transactions
- **Period:** December 2009 – December 2011
- **Original records:** 1,067,371
- **Original columns:** 8
- **Format:** Excel workbook

### Dataset columns

| Column | Description |
|---|---|
| Invoice | Transaction invoice number |
| StockCode | Product code |
| Description | Product description |
| Quantity | Number of units |
| InvoiceDate | Transaction date and time |
| Price | Unit selling price |
| Customer ID | Customer identifier |
| Country | Customer's country |

**Dataset citation:**

Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D

## 3. Data Preparation

The original workbook was preserved in `data/raw/`.

Initial data investigation identified:

- Missing customer IDs: 243,007
- Missing product descriptions: 4,382
- Negative quantities: 22,950
- Zero or negative prices: 6,207
- Cancelled invoices: 19,494

A provisional cleaning process separated records into two groups:

| Category | Records |
|---|---:|
| Initial cleaned sales subset | 1,041,670 |
| Records for review | 25,701 |
| Total original records | 1,067,371 |

Records with cancelled invoice numbers, non-positive quantities, or non-positive prices were separated for review.

The original data was not overwritten. Review records were retained separately for transparency and future investigation.

**Note:** This is an initial cleaned sales subset. Further validation of returns, unusual transactions and product descriptions may refine the cleaning rules.

## 4. Database Setup

The cleaned sales subset was imported into an SQLite database.

- Database: `database/fashionmind.db`
- Main table: `sales`
- Imported records: 1,041,670
- Database records verified: 1,041,670

Indexes were created on invoice, customer ID, product code and invoice date to support common analysis queries.

## 5. Key Business Metrics

| Metric | Result |
|---|---:|
| Records analysed | 1,041,670 |
| Total sales value | £20,972,594.57 |
| Units sold | 11,420,305 |
| Unique products | 4,917 |
| Unique customers | 5,878 |

**Revenue calculation:**

Quantity × Unit Selling Price

The reported sales value is gross transaction revenue calculated from the available fields. It is not net profit.

## 6. Key SQL Findings

### 6.1 Geographic Sales Performance

The United Kingdom generated approximately £17.87 million in sales, representing around 85.2% of the analysed sales value.

Other notable markets included:

- Ireland (EIRE): £664,431.78
- Netherlands: £554,232.34
- Germany: £431,262.46
- France: £356,944.60

**Business insight:** The UK was the dominant market in this historical dataset. Other countries may provide opportunities for further market-level analysis.

### 6.2 Monthly Sales Trends

The highest monthly sales values in the two complete calendar years shown were:

- November 2010: £1,470,272.48
- November 2011: £1,509,496.33

February recorded comparatively low sales:

- February 2010: £553,339.74
- February 2011: £523,631.89

**Business insight:** The repeated November peak suggests a possible seasonal sales pattern. Further analysis is needed before treating this as a reliable forecasting pattern.

### 6.3 Top Products by Revenue

After excluding several non-standard transaction codes, leading products included:

1. Regency Cake Stand 3 Tier — £344,563.25
2. White Hanging Heart T-Light Holder — £262,931.16
3. Paper Craft Little Birdie — £168,469.60
4. Party Bunting — £149,187.05
5. Jumbo Bag Red Retrospot — £148,823.92

**Business insight:** Product-level revenue analysis helps identify products that contribute significantly to sales value.

### 6.4 Top Products by Units Sold

Examples of high-volume products included:

- World War 2 Gliders — 110,138 units
- White Hanging Heart T-Light Holder — 96,086 units
- Assorted Colour Bird Ornament — 81,809 units
- Paper Craft Little Birdie — 80,995 units
- Jumbo Bag Red Retrospot — 78,860 units

**Business insight:** High sales volume and high revenue are not the same. Businesses should consider both when evaluating product performance.

### 6.5 Customer Purchasing Frequency

Customers were grouped by the number of distinct invoices:

| Segment | Customers |
|---|---:|
| One-time (1 invoice) | 1,623 |
| Occasional (2–5 invoices) | 2,454 |
| Regular (6–15 invoices) | 1,331 |
| Frequent (16+ invoices) | 470 |
| **Total** | **5,878** |

**Business insight:** The customer base contains different purchasing-frequency groups. These can support future retention and customer segmentation analysis.

This is a simplified frequency segmentation, not a complete RFM model.

### 6.6 Historical Customer Revenue

The analysis identified customers with high cumulative historical sales value.

For example, customer 18102 generated approximately £608,821.65 across 145 invoices.

**Business insight:** Historical customer revenue can help identify high-value customer relationships for further investigation.

This metric is not predictive customer lifetime value and does not represent customer profitability.

### 6.7 Product Data Quality

Several product codes were associated with multiple product descriptions.

This indicates a product-standardisation issue that may affect product-level reporting.

**Business insight:** A consistent product master is important for reliable product comparisons, dashboards and demand analysis.

### 6.8 Sales by Year

The analysis covered three calendar years:

- 2009: £825,685.76
- 2010: £10,303,952.40
- 2011: £9,842,956.40

The 2009 data covers only part of December. The 2011 data also requires caution because the dataset does not necessarily represent a complete December trading period.

Therefore, these yearly totals should not be interpreted as a like-for-like annual growth comparison.

## 7. Business Recommendations

Based on the initial analysis:

1. Monitor monthly sales trends to identify possible seasonal demand patterns.
2. Evaluate products using both revenue and units sold.
3. Investigate customer purchasing frequency to support retention strategies.
4. Standardise product codes and descriptions before building advanced product reports.
5. Review unusual and non-standard transaction records before using them in business decisions.
6. Develop more detailed demand analysis before making inventory-planning decisions.

## 8. Limitations

The current dataset has important limitations:

- It represents historical UK online retail transactions from 2009–2011, not current market conditions.
- It does not contain product purchase costs, so profit and profit margins cannot be calculated.
- It does not contain stock-on-hand quantities, so actual stockouts and overstock cannot be confirmed.
- It does not include supplier lead times or manufacturing information.
- It does not contain fashion attributes such as fabric, colour, silhouette or occasion.
- Missing customer IDs limit customer-level analysis.
- Product descriptions require further standardisation.
- The current cleaning process is provisional and review records need further investigation.

## 9. Next Development Stage

The next stage of FashionMind will focus on:

- Building a Power BI dashboard.
- Creating interactive sales and product-performance reports.
- Improving data quality and product standardisation.
- Developing customer segmentation.
- Exploring demand forecasting.
- Connecting analytical results to the FashionMind web application.

## 10. Conclusion

The initial SQL analysis transformed a large historical retail transaction dataset into structured business metrics and actionable areas for further investigation.

The findings demonstrate how SQL can support sales analysis, product evaluation, customer understanding and data-quality assessment.

FashionMind will build on this foundation by combining SQL, Python, Power BI and web development into an integrated retail intelligence platform.

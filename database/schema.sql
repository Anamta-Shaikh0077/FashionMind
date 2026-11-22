
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice TEXT,
    stock_code TEXT,
    description TEXT,
    quantity INTEGER,
    invoice_date TEXT,
    price REAL,
    customer_id TEXT,
    country TEXT
);

CREATE INDEX IF NOT EXISTS idx_sales_invoice
ON sales(invoice);

CREATE INDEX IF NOT EXISTS idx_sales_customer
ON sales(customer_id);

CREATE INDEX IF NOT EXISTS idx_sales_stock
ON sales(stock_code);

CREATE INDEX IF NOT EXISTS idx_sales_date
ON sales(invoice_date);

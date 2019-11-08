DROP TABLE IF EXISTS "xero_load_invoices";

CREATE TABLE IF NOT EXISTS "xero_load_invoices" (
  "Type" TEXT,
  "InvoiceID" TEXT,
  "InvoiceNumber" TEXT,
  "CurrencyRate" REAL,
  "Date" TEXT, -- format: YYYY-MM-DD e.g. 2019-01-01
  "Status" TEXT,
  "Total" REAL,
  "CurrencyCode" TEXT,
  "ContactID" TEXT
);

DROP TABLE IF EXISTS "xero_load_invoice_lineitems";

CREATE TABLE IF NOT EXISTS "xero_load_invoice_lineitems" (
  "LineItemID" TEXT,
  "InvoiceID" TEXT,
  "Description" TEXT,
  "UnitAmount" REAL,
  "LineAmount" REAL,
  "AccountCode" TEXT,
  "Quantity" REAL,
  "TaxType" TEXT DEFAULT 'NONE'
);

DROP TABLE IF EXISTS "xero_load_lineitem_tracking";

CREATE TABLE IF NOT EXISTS "xero_load_lineitem_tracking" (
  "Name" TEXT,
  "Option" TEXT,
  "LineItemID" TEXT
);

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

DROP TABLE IF EXISTS "xero_load_invoices_mapping";

CREATE TABLE IF NOT EXISTS "xero_load_invoices_mapping" (
  "InvoiceID" TEXT,
  "XeroInvoiceID" TEXT -- this is what is returned by Xero
);

DROP TABLE IF EXISTS "xero_load_invoice_lineitems";

CREATE TABLE IF NOT EXISTS "xero_load_invoice_lineitems" (
  "InvoiceID" TEXT, -- internal use only. Not sent to Xero
  "LineItemID" TEXT, -- internal use only. Not sent to Xero
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
  "LineItemID" TEXT -- internal use only. Not sent to Xero
);

DROP TABLE IF EXISTS "xero_load_invoices";

CREATE TABLE IF NOT EXISTS "xero_load_invoices" (
  "Type" TEXT not null,
  "InvoiceID" TEXT unique,
  "InvoiceNumber" TEXT,
  "Date" DATE not null, -- YYYY-MM-DD e.g. 2019-01-01
  "Status" TEXT,
  "Total" REAL not null,
  "CurrencyCode" TEXT,
  "ContactID" TEXT not null,
  "XeroInvoiceID" TEXT unique
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

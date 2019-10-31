DROP TABLE IF EXISTS "xero_load_invoices";
DROP TABLE IF EXISTS "xero_load_invoice_lineitems";
DROP TABLE IF EXISTS "xero_load_lineitem_tracking";

CREATE TABLE IF NOT EXISTS "xero_load_invoices" (
"Type" TEXT,
  "InvoiceID" TEXT,
  "InvoiceNumber" TEXT,
  "Reference" TEXT,
  "CurrencyRate" REAL,
  "DateString" DATE,
  "Date" TIMESTAMP,
  "Status" TEXT,
  "LineAmountTypes" TEXT,
  "Total" REAL,
  "UpdatedDateUTC" TIMESTAMP,
  "CurrencyCode" TEXT,
  "ContactID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_load_invoice_lineitems" (
  "LineItemID" TEXT,
  "InvoiceID" TEXT,
  "Description" TEXT,
  "UnitAmount" REAL,
  "LineAmount" REAL,
  "AccountCode" TEXT,
  "Quantity" REAL
);

CREATE TABLE IF NOT EXISTS "xero_load_lineitem_tracking" (
"Name" TEXT,
  "Option" TEXT,
  "TrackingCategoryID" TEXT,
  "TrackingOptionID" TEXT,
  "LineItemID" TEXT
);

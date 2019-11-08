DROP TABLE IF EXISTS "xero_extract_tracking_categories";
DROP TABLE IF EXISTS "xero_extract_tracking_options";
DROP TABLE IF EXISTS "xero_extract_contacts";
DROP TABLE IF EXISTS "xero_extract_invoices";
DROP TABLE IF EXISTS "xero_extract_invoice_lineitems";
DROP TABLE IF EXISTS "xero_extract_lineitem_tracking";
DROP TABLE IF EXISTS "xero_extract_accounts";

CREATE TABLE IF NOT EXISTS "xero_extract_trackingcategories" (
  "Name" TEXT,
  "Status" TEXT,
  "TrackingCategoryID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_trackingoptions" (
  "TrackingOptionID" TEXT,
  "Name" TEXT,
  "Status" TEXT,
  "TrackingCategoryID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_contacts" (
"ContactID" TEXT,
  "Name" TEXT,
  "ContactStatus" TEXT,
  "IsSupplier" INTEGER,
  "IsCustomer" INTEGER
);

CREATE TABLE IF NOT EXISTS "xero_extract_invoices" (
"Type" TEXT,
  "InvoiceID" TEXT,
  "InvoiceNumber" TEXT,
  "Reference" TEXT,
  "CurrencyRate" REAL,
  "Date" TIMESTAMP,
  "Status" TEXT,
  "LineAmountTypes" TEXT,
  "Total" REAL,
  "UpdatedDateUTC" TIMESTAMP,
  "CurrencyCode" TEXT,
  "ContactID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_invoice_lineitems" (
  "LineItemID" TEXT,
  "InvoiceID" TEXT,
  "Description" TEXT,
  "UnitAmount" REAL,
  "LineAmount" REAL,
  "AccountCode" TEXT,
  "Quantity" REAL
);

CREATE TABLE IF NOT EXISTS "xero_extract_lineitem_tracking" (
"Name" TEXT,
  "Option" TEXT,
  "TrackingCategoryID" TEXT,
  "TrackingOptionID" TEXT,
  "LineItemID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_accounts" (
"AccountID" TEXT,
  "Code" TEXT,
  "Name" TEXT,
  "Status" TEXT,
  "Type" TEXT,
  "CurrencyCode" TEXT
);
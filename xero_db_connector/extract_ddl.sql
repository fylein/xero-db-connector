DROP TABLE IF EXISTS "xero_extract_trackingcategories";
DROP TABLE IF EXISTS "xero_extract_trackingoptions";
DROP TABLE IF EXISTS "xero_extract_contacts";
DROP TABLE IF EXISTS "xero_extract_invoices";
DROP TABLE IF EXISTS "xero_extract_invoice_lineitems";
DROP TABLE IF EXISTS "xero_extract_lineitem_tracking";
DROP TABLE IF EXISTS "xero_extract_accounts";

CREATE TABLE IF NOT EXISTS "xero_extract_trackingcategories" (
  "Name" TEXT not null unique,
  "Status" TEXT,
  "TrackingCategoryID" TEXT not null unique
);

CREATE TABLE IF NOT EXISTS "xero_extract_trackingoptions" (
  "TrackingOptionID" TEXT not null unique,
  "Name" TEXT,
  "Status" TEXT,
  "TrackingCategoryID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_contacts" (
  "ContactID" TEXT not null unique,
  "Name" TEXT not null unique,
  "ContactStatus" TEXT,
  "IsSupplier" INTEGER,
  "IsCustomer" INTEGER
);

CREATE TABLE IF NOT EXISTS "xero_extract_invoices" (
  "Type" TEXT,
  "InvoiceID" TEXT not null unique,
  "InvoiceNumber" TEXT,
  "Reference" TEXT,
  "Date" TIMESTAMP,
  "Status" TEXT,
  "LineAmountTypes" TEXT,
  "Total" REAL,
  "UpdatedDateUTC" TIMESTAMP,
  "CurrencyCode" TEXT,
  "ContactID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_invoice_lineitems" (
  "LineItemID" TEXT not null unique,
  "InvoiceID" TEXT not null,
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
  "AccountID" TEXT not null unique,
  "Code" TEXT not null unique,
  "Name" TEXT,
  "Status" TEXT,
  "Type" TEXT,
  "CurrencyCode" TEXT
);
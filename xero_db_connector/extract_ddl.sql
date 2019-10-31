DROP TABLE IF EXISTS "xero_extract_tracking_categories";
DROP TABLE IF EXISTS "xero_extract_tracking_options";
DROP TABLE IF EXISTS "xero_extract_contacts";
DROP TABLE IF EXISTS "xero_extract_invoices";
DROP TABLE IF EXISTS "xero_extract_invoice_lineitems";
DROP TABLE IF EXISTS "xero_extract_lineitem_tracking";
DROP TABLE IF EXISTS "xero_extract_accounts";

CREATE TABLE IF NOT EXISTS "xero_extract_tracking_categories" (
"Name" TEXT,
  "Status" TEXT,
  "TrackingCategoryID" TEXT
);

CREATE TABLE IF NOT EXISTS "xero_extract_tracking_options" (
"TrackingOptionID" TEXT,
  "Name" TEXT,
  "Status" TEXT,
  "TrackingCategoryId" TEXT
);
CREATE TABLE IF NOT EXISTS "xero_extract_contacts" (
"ContactID" TEXT,
  "Name" TEXT,
  "ContactStatus" TEXT,
  "EmailAddress" TEXT,
  "IsSupplier" INTEGER,
  "IsCustomer" INTEGER
);
CREATE TABLE IF NOT EXISTS "xero_extract_invoices" (
"Type" TEXT,
  "InvoiceID" TEXT,
  "InvoiceNumber" TEXT,
  "Reference" TEXT,
  "AmountDue" REAL,
  "AmountPaid" REAL,
  "AmountCredited" REAL,
  "CurrencyRate" REAL,
  "IsDiscounted" INTEGER,
  "HasAttachments" INTEGER,
  "HasErrors" INTEGER,
  "DateString" DATE,
  "Date" TIMESTAMP,
  "DueDateString" DATE,
  "DueDate" TIMESTAMP,
  "BrandingThemeID" TEXT,
  "Status" TEXT,
  "LineAmountTypes" TEXT,
  "SubTotal" REAL,
  "TotalTax" REAL,
  "Total" REAL,
  "UpdatedDateUTC" TIMESTAMP,
  "CurrencyCode" TEXT,
  "ContactID" TEXT,
  "FullyPaidOnDate" TIMESTAMP,
  "SentToContact" INTEGER
);
CREATE TABLE IF NOT EXISTS "xero_extract_invoice_lineitems" (
"Description" TEXT,
  "UnitAmount" REAL,
  "TaxType" TEXT,
  "TaxAmount" REAL,
  "LineAmount" REAL,
  "AccountCode" TEXT,
  "Quantity" REAL,
  "LineItemID" TEXT,
  "InvoiceID" TEXT,
  "ItemCode" TEXT
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
  "CurrencyCode" TEXT,
  "Description" TEXT
);
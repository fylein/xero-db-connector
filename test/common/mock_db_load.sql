-- invoices

insert into xero_load_invoices ("Type", "InvoiceID", "InvoiceNumber", "Date", "Status", "Total", "CurrencyCode", "ContactID") 
values('ACCPAY', 'I1', 'C/2019/09/R/1069', '2019-09-01', 'DRAFT', 200.0, 'USD', '78b7299c-4f1f-46d2-acc3-44a46bd361b1');
insert into xero_load_invoices ("Type", "InvoiceID", "InvoiceNumber", "Date", "Status", "Total", "CurrencyCode", "ContactID") 
values('ACCPAY', 'I2', 'C/2019/09/R/1070', '2019-10-01', 'DRAFT', 200.0, 'USD', '78b7299c-4f1f-46d2-acc3-44a46bd361b1');

-- invoice_lineitems

insert into xero_load_invoice_lineitems ("InvoiceID", "LineItemID", "Description", "UnitAmount", "LineAmount", "AccountCode", "Quantity", "TaxType") 
values('I1', '1', 'Yabadabadoo', 100.0, 100.0, 453, 1.0, 'NONE');
insert into xero_load_invoice_lineitems ("InvoiceID", "LineItemID", "Description", "UnitAmount", "LineAmount", "AccountCode", "Quantity", "TaxType") 
values('I1', '2', 'Bada bing', 100.0, 100.0, 453, 1.0, 'NONE');
insert into xero_load_invoice_lineitems ("InvoiceID", "LineItemID", "Description", "UnitAmount", "LineAmount", "AccountCode", "Quantity", "TaxType") 
values('I2', '3', 'Yabadabadoo', 100.0, 100.0, 453, 1.0, 'NONE');
insert into xero_load_invoice_lineitems ("InvoiceID", "LineItemID", "Description", "UnitAmount", "LineAmount", "AccountCode", "Quantity", "TaxType") 
values('I2', '4', 'Bada bing', 100.0, 100.0, 453, 1.0, 'NONE');

-- tracking code

insert into xero_load_lineitem_tracking ("Name", "Option", "LineItemID")
values('Region', 'North', '1');
insert into xero_load_lineitem_tracking ("Name", "Option", "LineItemID")
values('Region', 'Eastside', '1');

insert into xero_load_lineitem_tracking ("Name", "Option", "LineItemID" )
values('Region', 'North', '3');
insert into xero_load_lineitem_tracking ("Name", "Option", "LineItemID")
values('Region', 'Eastside', '4');


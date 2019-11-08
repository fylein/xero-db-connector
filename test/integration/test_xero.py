import pytest
import logging
from common.utilities import dict_compare_keys

logger = logging.getLogger(__name__)

def test_contacts(xero, mock_xero):
    contacts = xero.contacts.all()
    mock_contacts = mock_xero.contacts.all()

    assert dict_compare_keys(contacts[0], mock_contacts[0]) == [], 'xero.contacts.all() has stuff that mock_xero doesnt'
    assert dict_compare_keys(mock_contacts[0], contacts[0]) == [], 'mock_xero.contacts.all() has stuff that xero doesnt'

def test_accounts(xero, mock_xero):
    accounts = xero.accounts.all()
    mock_accounts = mock_xero.accounts.all()

    assert dict_compare_keys(accounts[0], mock_accounts[0]) == [], 'xero.accounts.all() has stuff that mock_xero doesnt'
    assert dict_compare_keys(mock_accounts[0], accounts[0]) == [], 'mock_xero.accounts.all() has stuff that xero doesnt'

def test_trackingcategories(xero, mock_xero):
    trackingcategories = xero.trackingcategories.all()
    mock_trackingcategories = mock_xero.trackingcategories.all()

    assert dict_compare_keys(trackingcategories[0], mock_trackingcategories[0]) == [], 'xero.trackingcategories.all() has stuff that mock_xero doesnt'
    assert dict_compare_keys(mock_trackingcategories[0], trackingcategories[0]) == [], 'mock_xero.accounts.all() has stuff that xero doesnt'

def test_invoices(xero, mock_xero):
    invoices = xero.invoices.all()
    mock_invoices = mock_xero.invoices.all()

    assert dict_compare_keys(invoices[0], mock_invoices[0]) == [], 'xero.invoices.all() has stuff that mock_xero doesnt'
    assert dict_compare_keys(mock_invoices[0], invoices[0]) == [], 'mock_xero.accounts.all() has stuff that xero doesnt'

    invoices = xero.invoices.get(invoices[0]['InvoiceID'])
    mock_invoices = mock_xero.invoices.get('foo')

    assert dict_compare_keys(invoices[0], mock_invoices[0]) == [], 'xero.invoices.get() has stuff that mock_xero doesnt'
    assert dict_compare_keys(mock_invoices[0], invoices[0]) == [], 'mock_xero.accounts.get() has stuff that xero doesnt'

# def test_extract_contacts():
#     contact_ids = xec.extract_contacts()
#     assert contact_ids, 'No contacts extracted from xero account'
#     assert num_table_rows('xero_extract_contacts') == len(contact_ids), 'Not all contact ids are in the table'

# def test_extract_accounts():
#     account_ids = xec.extract_accounts()
#     assert account_ids, 'No accounts extracted from xero account'
#     assert num_table_rows('xero_extract_accounts') == len(account_ids), 'Not all account ids are in the table'

# def test_extract_tracking_categories():
#     tc = xec.extract_tracking_categories()
#     assert tc, 'No tracking categories in xero account'
#     assert num_table_rows('xero_extract_tracking_categories') > 0, 'No tracking category rows'
#     assert num_table_rows('xero_extract_tracking_options') > 0, 'No tracking options'

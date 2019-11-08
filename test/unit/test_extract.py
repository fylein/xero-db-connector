import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_xero_empty)
from xero_db_connector.extract import XeroExtractConnector

logger = logging.getLogger(__name__)

def test_contacts(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    ids = xec.extract_contacts()
    xero_data = xero.contacts.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_contacts')
    assert dict_compare_keys(db_data, xero_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_contacts') == len(xero.contacts.all()), 'row count mismatch'
    assert len(ids) == 44, 'return value messed up'

def test_accounts(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    ids = xec.extract_accounts()
    xero_data = xero.accounts.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_accounts')
    assert dict_compare_keys(db_data, xero_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_accounts') == len(xero.accounts.all()), 'row count mismatch'
    assert len(ids) == 58, 'return value messed up'

def test_trackingcategories(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    ids = xec.extract_trackingcategories()
    xero_data = xero.trackingcategories.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_trackingcategories')
    assert dict_compare_keys(db_data, xero_data) == [], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_trackingcategories') == len(xero.trackingcategories.all()), 'row count mismatch'
    assert ids == ['fa437cfd-f005-4538-ae84-943857da5c8c'], 'return value messed up'

def test_trackingoptions(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    ids = xec.extract_trackingcategories()
    xero_data = xero.trackingcategories.all()[0]['Options'][0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_trackingoptions')
    assert dict_compare_keys(db_data, xero_data) == ['->TrackingCategoryID'], 'db table has some columns that xero doesnt'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_trackingoptions') == len(xero.trackingcategories.all()[0]['Options']), 'row count mismatch'

def test_invoices(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    ids = xec.extract_invoices()
    xero_data = xero.invoices.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_invoices')
    assert dict_compare_keys(db_data, xero_data) == [], 'db table has some columns that xero doesnt'
    assert ids == ['9f5bca33-8590-4b6f-acfb-e85712b10217'], 'return value messed up'

def test_datetime(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xec.extract_invoices()
    invoice = dbconn_table_row_dict(dbconn, 'xero_extract_invoices')
    assert invoice['Date'].isoformat() == '2019-10-09T00:00:00'
    assert invoice['UpdatedDateUTC'].isoformat() == '2008-12-20T16:40:33'

def test_empty(dbconn):
    xero = get_mock_xero_empty()
    res = XeroExtractConnector(xero=xero, dbconn=dbconn)
    res.create_tables()
    assert res.extract_accounts() == []
    assert res.extract_contacts() == []
    assert res.extract_trackingcategories() == []
    assert res.extract_invoices() == []

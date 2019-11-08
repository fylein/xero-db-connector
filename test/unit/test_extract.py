import pytest

import sqlite3
import logging
from os import path
import json
from common.utilities import dict_compare_keys, dbconn_table_num_rows, dbconn_table_row_dict

logger = logging.getLogger(__name__)

def test_contacts(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    xec.extract_contacts()
    xero_data = xero.contacts.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_contacts')
    assert dict_compare_keys(db_data, xero_data) == [], 'db_data has something that xero doesnt'

def test_accounts(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    xec.extract_accounts()
    xero_data = xero.accounts.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_accounts')
    assert dict_compare_keys(db_data, xero_data) == [], 'db_data has something that xero doesnt'

def test_trackingcategories(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    xec.extract_trackingcategories()
    xero_data = xero.trackingcategories.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_trackingcategories')
    assert dict_compare_keys(db_data, xero_data) == [], 'db_data has something that xero doesnt'

def test_trackingoptions(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    xec.extract_trackingcategories()
    xero_data = xero.trackingcategories.all()[0]['Options'][0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_trackingoptions')
    assert dict_compare_keys(db_data, xero_data) == ['->TrackingCategoryID'], 'db_data has something that xero doesnt'

def test_invoices(xec):
    dbconn = xec._XeroExtractConnector__dbconn
    xero = xec._XeroExtractConnector__xero
    xec.extract_invoices()
    xero_data = xero.invoices.all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'xero_extract_invoices')
    assert dict_compare_keys(db_data, xero_data) == [], 'db_data has something that xero doesnt'


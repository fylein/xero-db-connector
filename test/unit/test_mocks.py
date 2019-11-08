import pytest

import sqlite3
import logging
from os import path
import json
from unittest.mock import Mock
from common.utilities import dict_compare_keys, dbconn_table_num_rows

logger = logging.getLogger(__name__)

def test_xero_mock_setup(xero):
    assert xero.invoices.get('232')[0]['InvoiceID'] == '9f5bca33-8590-4b6f-acfb-e85712b10217', 'xero mock setup is broken'
    assert xero.invoices.all()[0]['LineItems'] == [], 'xero invoices all returns empty lineitems'
    assert xero.invoices.get('232')[0]['LineItems'] != [], 'xero invoices get should not return empty lineitems'

def test_dbconn_mock_setup(dbconn):
    with pytest.raises(sqlite3.OperationalError) as e:
        rows = dbconn_table_num_rows(dbconn, 'xero_extract_accounts')

def test_xec_mock_setup(xec):
    # python magic to access private variable for testing db state
    dbconn = xec._XeroExtractConnector__dbconn
    assert dbconn_table_num_rows(dbconn, 'xero_extract_accounts') == 0, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_trackingcategories') == 0, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'xero_extract_contacts') == 0, 'Unclean db'

def test_dict_compare():
    d1 = {
        'k1' : 'xxx', 'k2' : 2, 'k3' : [1, 2], 'k4' : { 'k41' : [2], 'k42' : { 'k421' : 20}}
    }
    d2 = {
        'k1' : 'xyx', 'k3' : [1, 2], 'k4' : { 'k42' : { 'k421' : 20}}
    }
    d3 = {
        'k1' : 'xyz', 'k3' : [3, 2], 'k4' : { 'k42' : { 'k421' : 40}}
    }
    assert dict_compare_keys(d1, d2) == ['->k2', '->k4->k41'], 'not identifying diff properly'
    assert dict_compare_keys(d2, d3) == [], 'should return no diff'
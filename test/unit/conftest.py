import json
import logging
import os
import sqlite3
from os import path
from unittest.mock import Mock

import pytest

from common.utilities import get_mock_xero_dict
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

@pytest.fixture
def xero():
    mock_xero_dict = get_mock_xero_dict()
    mock_xero = Mock()
    mock_xero.contacts.all.return_value = mock_xero_dict['contacts']
    mock_xero.trackingcategories.all.return_value = mock_xero_dict['trackingcategories']
    mock_xero.invoices.all.return_value = mock_xero_dict['invoices_all']
    mock_xero.invoices.filter.return_value = mock_xero_dict['invoices_all']
    mock_xero.invoices.get.return_value = mock_xero_dict['invoices_get']
    mock_xero.accounts.all.return_value = mock_xero_dict['accounts']
    return mock_xero

@pytest.fixture
def dbconn():
    SQLITE_DB_FILE = '/tmp/test_xero.db'
    if os.path.exists(SQLITE_DB_FILE):
        os.remove(SQLITE_DB_FILE)
    return sqlite3.connect(SQLITE_DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

@pytest.fixture
def xec(xero, dbconn):
    res = XeroExtractConnector(xero=xero, dbconn=dbconn)
    res.create_tables()
    return res

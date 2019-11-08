import json
import logging
import os
import sqlite3
from os import path

import pytest

from common.utilities import get_mock_xero, xero_connect
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

@pytest.fixture
def mock_xero():
    return get_mock_xero()

@pytest.fixture(scope='module')
def xero():
    return xero_connect()

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

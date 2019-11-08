import json
import logging
import os
import sqlite3
from os import path
from unittest.mock import Mock

import pytest

from common.utilities import get_mock_xero
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

@pytest.fixture
def xero():
    return get_mock_xero()

@pytest.fixture
def dbconn():
    SQLITE_DB_FILE = '/tmp/test_xero.db'
    if os.path.exists(SQLITE_DB_FILE):
        os.remove(SQLITE_DB_FILE)
    conn = sqlite3.connect(SQLITE_DB_FILE)
    return conn

@pytest.fixture
def xec(xero, dbconn):
    res = XeroExtractConnector(xero=xero, dbconn=dbconn)
    res.create_tables()
    return res

@pytest.fixture
def xlc(xero, dbconn):
    res = XeroLoadConnector(xero=xero, dbconn=dbconn)
    res.create_tables()
    basepath = path.dirname(__file__)
    sqlpath = path.join(basepath, '../common/mock_db_load.sql')
    sql = open(sqlpath, 'r').read()
    dbconn.executescript(sql)
    return res

import pytest

import sqlite3
import logging
import os
from os import path
import json
from xero import Xero
from xero.auth import PrivateCredentials
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

@pytest.fixture
def xero():
    XERO_PRIVATE_KEYFILE = os.environ.get('XERO_PRIVATE_KEYFILE', None)
    XERO_CONSUMER_KEY = os.environ.get('XERO_CONSUMER_KEY', None)

    if XERO_PRIVATE_KEYFILE is None:
        raise Exception('XERO_PRIVATE_KEYFILE is not set')

    if XERO_CONSUMER_KEY is None:
        raise Exception('XERO_CONSUMER_KEY is not set')

    with open(XERO_PRIVATE_KEYFILE) as keyfile:
        rsa_key = keyfile.read()

    credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)
    # used to connect to xero
    return Xero(credentials)

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
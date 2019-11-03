import os
import sqlite3

from xero import Xero
from xero.auth import PrivateCredentials

from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector

XERO_PRIVATE_KEYFILE = os.environ.get('XERO_PRIVATE_KEYFILE', None)
XERO_CONSUMER_KEY = os.environ.get('XERO_CONSUMER_KEY', None)

class XeroCredentialsError(Exception):
    ''' Any initialization errors
    '''
    pass

if XERO_PRIVATE_KEYFILE is None:
    raise XeroCredentialsError('XERO_PRIVATE_KEYFILE is not set')

if XERO_CONSUMER_KEY is None:
    raise XeroCredentialsError('XERO_CONSUMER_KEY is not set')

with open(XERO_PRIVATE_KEYFILE) as keyfile:
    rsa_key = keyfile.read()

credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)

# used to connect to xero
xero = Xero(credentials)

# connection to sqlite db - always delete the file if it exists already
SQLITE_DB_FILE = '/tmp/test_xero.db'
if os.path.exists(SQLITE_DB_FILE):
    os.remove(SQLITE_DB_FILE)
dbconn = sqlite3.connect(SQLITE_DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

# connectors that will be used in tests
xec = XeroExtractConnector(xero=xero, dbconn=dbconn)
xlc = XeroLoadConnector(xero=xero, dbconn=dbconn)

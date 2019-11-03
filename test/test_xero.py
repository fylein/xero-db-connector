import pytest

import sqlite3
import logging
from . import xero, xec, xlc, dbconn

logger = logging.getLogger(__name__)

# def test_xero_connection()

# dbconn = sqlite3.connect("/tmp/xero.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
# e = XeroExtractConnector(xero=xero, dbconn=dbconn)
# l = XeroLoadConnector(xero=xero, dbconn=dbconn)

# def create_tables():
#     global e, l
#     e.create_tables()
#     l.create_tables()

# def extract():
#     global e, l
#     e.extract_accounts()
#     e.extract_contacts()
#     e.extract_tracking_categories()

# def transform():
#     pass

# def load():
#     global e, l
#     x.load_invoice(invoice_id='I1')
#     x.load_invoice(invoice_id='I2')

def num_table_rows(tablename):
    query = f'select count(*) from {tablename}'
    return dbconn.cursor().execute(query).fetchone()[0]

def test_xero_connection():
    contacts = xero.contacts.all()
    assert xero.contacts.all(), 'Unable to contact Xero'

def test_extract_accounts():
    account_ids = xec.extract_accounts()
    assert account_ids, 'No accounts extracted from xero account'
    assert num_table_rows('xero_extract_accounts') == len(account_ids), 'Not all account ids are in the table'

def test_extract_tracking_categories():
    tc = xec.extract_tracking_categories()
    assert tc, 'No tracking categories in xero account'
    assert num_table_rows('xero_extract_tracking_categories') > 0, 'No tracking category rows'
    assert num_table_rows('xero_extract_tracking_options') > 0, 'No tracking options'
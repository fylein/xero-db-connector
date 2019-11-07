import pytest
import logging

logger = logging.getLogger(__name__)

def test_connection(xero):
    contacts = xero.contacts.all()
    logger.info('got %d contacts', len(contacts))
    assert xero.contacts.all(), 'Unable to contact Xero'

# def test_contacts(mocker):
#     ['ContactID', 'Name', 'ContactStatus', 'EmailAddress', 'IsSupplier', 'IsCustomer']

#     pass

# def test_tracking_categories(mocker):
#     ['TrackingCategoryID', 'Name', 'Status']

#     pass


# def num_table_rows(tablename):
#     query = f'select count(*) from {tablename}'
#     return dbconn.cursor().execute(query).fetchone()[0]


# def test_tables_exist():
#     assert num_table_rows('xero_extract_accounts') == 0, 'Unclean db'
#     assert num_table_rows('xero_extract_tracking_categories') == 0, 'Unclean db'
#     assert num_table_rows('xero_extract_contacts') == 0, 'Unclean db'

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

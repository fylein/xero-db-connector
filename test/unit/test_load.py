import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_xero_empty)
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

def test_load_invoice_generator(xel):
    invoice_ids = list(xel.load_invoices_generator())
    assert invoice_ids == ['I1', 'I2'], 'invoice ids are incorrect'
 
import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_xero_empty)
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

def test_load_no_data(xlc):
    xero = xlc._XeroLoadConnector__xero
    dbconn = xlc._XeroLoadConnector__dbconn
    dbconn.cursor().execute('delete from xero_load_invoices')
    dbconn.commit()
    invoice_ids = list(xlc.load_invoices_generator())
    assert invoice_ids == [], 'invoice ids are incorrect'

def test_load_invoice_generator(xlc):
    xero = xlc._XeroLoadConnector__xero
    invoice_ids = list(xlc.load_invoices_generator())
    xero.invoices.save.assert_called()
    assert invoice_ids == ['I1', 'I2'], 'invoice ids are incorrect'
    assert xlc.get_xero_invoice_id('I1') == '9f5bca33-8590-4b6f-acfb-e85712b10217', 'xero invoice id not matching'

def test_get_xero_invoice_id(xlc):
    assert not xlc.get_xero_invoice_id('I1'), 'xero invoice id should not exist'
    list(xlc.load_invoices_generator())
    assert xlc.get_xero_invoice_id('I1') == '9f5bca33-8590-4b6f-acfb-e85712b10217', 'xero invoice id not matching'
 
import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_xero_empty)
from xero_db_connector.load import XeroLoadConnector

logger = logging.getLogger(__name__)

def test_load_get_invoice_ids(xlc):
    dbconn = xlc._XeroLoadConnector__dbconn
    invoice_ids = xlc.get_invoice_ids()
    assert invoice_ids == ['I1', 'I2'], 'invoice ids are incorrect'

    dbconn.cursor().execute('delete from xero_load_invoices')
    dbconn.commit()
    invoice_ids = xlc.get_invoice_ids()
    assert invoice_ids == [], 'invoice ids are incorrect'

def test_load_invoice_generator(xlc):
    xero = xlc._XeroLoadConnector__xero
    xlc.load_invoice(invoice_id='I2')
    xero.invoices.save.assert_called()
    invoice_posted = xero.invoices.save.call_args[0][0]
    assert invoice_posted['Date'].isoformat() == '2019-10-01'
    assert len(invoice_posted['LineItems']) == 2
    assert len(invoice_posted['LineItems'][0]['Tracking']) == 1
    assert xlc.get_xero_invoice_id('I2') == '9f5bca33-8590-4b6f-acfb-e85712b10217', 'xero invoice id not matching'

def test_get_xero_invoice_id(xlc):
    assert not xlc.get_xero_invoice_id('I1'), 'xero invoice id should not exist'
    xlc.load_invoice(invoice_id='I1')
    assert xlc.get_xero_invoice_id('I1') == '9f5bca33-8590-4b6f-acfb-e85712b10217', 'xero invoice id not matching'



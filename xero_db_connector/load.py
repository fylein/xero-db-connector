"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from os import path
from typing import List

import pandas as pd
import sqlite3

logger = logging.getLogger('XeroLoadConnector')

class XeroLoadConnector:
    """
    - Extract Data from Database and load to Xero
    """
    def __init__(self, xero, dbconn):
        self.__xero = xero
        self.__dbconn = dbconn
        self.__dbconn.row_factory = sqlite3.Row

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'load_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)
   
    def load_invoice(self, invoice_id) -> str:
        """
        Load a single invoice to xero and returns invoice_id. This also updates the column InvoiceID in the table
        """
        invoice_rs = self.__dbconn.cursor().execute('select * from xero_load_invoices where "InvoiceID" = ?', (invoice_id,)).fetchone()
        assert invoice_rs, 'Invoice not found'
        invoice = dict(invoice_rs)
        del invoice['InvoiceID']
#        del invoice['Date']
        invoice['Contact'] = {'ContactID': invoice['ContactID']}
        del invoice['ContactID']
        lineitems = []
        for lr in self.__dbconn.cursor().execute('select * from xero_load_invoice_lineitems where "InvoiceID" = ?', (invoice_id,)):
            lineitem = dict(lr)
            trackings = []
            for tr in self.__dbconn.cursor().execute('select * from xero_load_lineitem_tracking where "LineItemID" = ?', (lineitem['LineItemID'],)):
                tracking = dict(tr)
                del tracking['LineItemID']
                trackings.append(tracking)
            lineitem['Tracking'] = trackings
            del lineitem['InvoiceID']
            del lineitem['LineItemID']
            lineitems.append(lineitem)
        invoice['LineItems'] = lineitems
        logger.info('complete invoice %s', str(invoice))
        r = self.__xero.invoices.save(invoice)[0]
        logger.debug('return object %s', str(r))
        new_invoice_id = r['InvoiceID']
        self.__dbconn.cursor().execute('update xero_load_invoices set "InvoiceID"=? where "InvoiceID"=?', (new_invoice_id, invoice_id,))
        return new_invoice_id


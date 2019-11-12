"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from os import path
from typing import Generator

import sqlite3

class XeroLoadConnector:
    """
    - Extract Data from Database and load to Xero
    """
    def __init__(self, xero, dbconn):
        self.__xero = xero
        self.__dbconn = dbconn
        self.__dbconn.row_factory = sqlite3.Row
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'load_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)
    
    def get_invoice_ids(self):
        """
        Returns list of invoice_ids
        """
        rows = self.__dbconn.cursor().execute('select "InvoiceID" from xero_load_invoices').fetchall()
        if not rows:
            return []
        return [row['InvoiceID'] for row in rows]

    def get_xero_invoice_id(self, invoice_id):
        """
        Get xero_invoice_id from invoices table
        """
        row = self.__dbconn.cursor().execute('select "XeroInvoiceID" from xero_load_invoices where "InvoiceID" = ?', (invoice_id,)).fetchone()
        if not row:
            return None
        return row['XeroInvoiceID']

    def load_invoice(self, invoice_id: str):
        """
        Loads invoices to xero and returns list of invoice_id. This also updates the column InvoiceID in the table
        """
        rows = self.__dbconn.cursor().execute('select * from xero_load_invoices where "InvoiceID" = ?', (invoice_id, )).fetchall()
        if not rows:
            return
        assert len(rows) == 1, 'Duplicate invoice_id'
        row = rows[0]
        invoice = dict(row)
        invoice_id = invoice['InvoiceID']
        del invoice['InvoiceID']
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
        self.logger.debug('complete invoice %s', str(invoice))
        r = self.__xero.invoices.save(invoice)[0]
        self.logger.debug('return object %s', str(r))
        xero_invoice_id = r['InvoiceID']
        self.__dbconn.cursor().execute('update xero_load_invoices set "XeroInvoiceID" = ? where "InvoiceID" = ?', (xero_invoice_id, invoice_id,))
        self.__dbconn.commit()
        self.logger.info('Loaded invoice = %s, xero_invoice_id = %s', invoice_id, xero_invoice_id)
        return xero_invoice_id

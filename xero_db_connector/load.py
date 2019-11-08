"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from os import path
from typing import List, Generator

import pandas as pd
import sqlite3
import copy

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
   
    def load_invoices_generator(self) -> Generator[str, None, None]:
        """
        Loads invoices to xero and returns list of invoice_id. This also updates the column InvoiceID in the table
        """
        rows = self.__dbconn.cursor().execute('select * from xero_load_invoices').fetchall()
        # invoice_ids = [row[0] for row in rows]
        # for invoice_id in invoice_ids:
        #     yield invoice_id
        if not rows:
            return

        for row in rows:
            invoice = dict(row)
            old_invoice = copy.deepcopy(invoice)
            old_invoice_id = invoice['InvoiceID']
            del invoice['InvoiceID']
            invoice['Contact'] = {'ContactID': invoice['ContactID']}
            del invoice['ContactID']
            lineitems = []
            for lr in self.__dbconn.cursor().execute('select * from xero_load_invoice_lineitems where "InvoiceID" = ?', (old_invoice_id,)):
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
#            r = self.__xero.invoices.save(invoice)[0]
            r = old_invoice
            logger.debug('return object %s', str(r))
            new_invoice_id = r['InvoiceID']
            # should probably have a separate column for this instead of updating in place
            self.__dbconn.cursor().execute('update xero_load_invoices set "InvoiceID"=? where "InvoiceID"=?', (new_invoice_id, old_invoice_id,))
            yield old_invoice_id


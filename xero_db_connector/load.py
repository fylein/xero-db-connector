"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from os import path
from typing import List, Generator

import pandas as pd
import sqlite3
import copy

logger = logging.getLogger(__file__)

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
   
    def get_xero_invoice_id(self, invoice_id):
        """
        Looks up the invoice id returned by Xero using internal invoice id
        """
        rows = self.__dbconn.cursor().execute('select "XeroInvoiceID" from xero_load_invoices_mapping where "InvoiceID" = ?', (invoice_id, )).fetchone()
        if not rows:
            return None       
        return rows[0]

    def load_invoices_generator(self) -> Generator[str, None, None]:
        """
        Loads invoices to xero and returns list of invoice_id. This also updates the column InvoiceID in the table
        """
        rows = self.__dbconn.cursor().execute('select * from xero_load_invoices').fetchall()
        if not rows:
            return

        for row in rows:
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
            logger.debug('complete invoice %s', str(invoice))
            r = self.__xero.invoices.save(invoice)[0]
            logger.debug('return object %s', str(r))
            xero_invoice_id = r['InvoiceID']
            self.__dbconn.cursor().execute('insert into xero_load_invoices_mapping("InvoiceID", "XeroInvoiceID") values(?, ?)', (invoice_id, xero_invoice_id,))
            self.__dbconn.commit()
            yield invoice_id

"""
XeroExtractConnector(): Connection between Xero and Database
"""

import logging
import sqlite3
import time
from os import path
from typing import List
import copy

import pandas as pd

logger = logging.getLogger('XeroExtractConnector')

class XeroExtractConnector:
    """
    - Extract Data from Xero and load to Database
    """
    def __init__(self, xero, dbconn):
        self.__dbconn = dbconn
        self.__xero = xero
        self.__dbconn.row_factory = sqlite3.Row

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'extract_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)

    def extract_contacts(self) -> List[str]:
        """
        Extract contacts from Xero
        :return: List of contact ids
        """
        logger.debug('extracting contacts from Xero')
        contacts = self.__xero.contacts.all()
        if not contacts:
            return []
        df_contacts = pd.DataFrame(contacts)
        df_contacts = df_contacts[['ContactID', 'Name', 'ContactStatus', 'IsSupplier', 'IsCustomer']]
        df_contacts.to_sql('xero_extract_contacts', self.__dbconn, if_exists='append', index=False)
        return df_contacts['ContactID'].to_list()

    def extract_trackingcategories(self) -> List[str]:
        """
        Extract tracking options from Xero
        :return: List of tracking option ids
        """
        logger.debug('extracting tracking from Xero')
        trackingcategories = self.__xero.trackingcategories.all()
        logger.debug('trackingcategories = %s', str(trackingcategories))
        if not trackingcategories:
            return []
        # tracking categories is a nested structure - so we get two flatted ones and create two tables
        tcl = []
        tol = []
        for tc in trackingcategories:
            options = copy.deepcopy(tc['Options'])
            tcl.append(tc)
            for to in options:
                to['TrackingCategoryID'] = tc['TrackingCategoryID']
                tol.append(to)
        df_tcl = pd.DataFrame(tcl)
        df_tcl = df_tcl[['TrackingCategoryID', 'Name', 'Status']]
        df_tcl.to_sql('xero_extract_trackingcategories', self.__dbconn, if_exists='append', index=False)
        df_tol = pd.DataFrame(tol)
        df_tol = df_tol[['TrackingOptionID', 'Name', 'Status', 'TrackingCategoryID']]
        df_tol.to_sql('xero_extract_trackingoptions', self.__dbconn, if_exists='append', index=False)
        return df_tcl['TrackingCategoryID'].to_list()

    def extract_accounts(self) -> List[str]:
        """
        Extract accounts from Xero
        :return: List of account ids
        """
        logger.debug('extracting accounts from Xero')
        accounts = self.__xero.accounts.all()
        logger.debug('accounts = %s', str(accounts))
        if not accounts:
            return []
        df_accounts = pd.DataFrame(accounts)
        df_accounts = df_accounts[['AccountID', 'Code', 'Name', 'Status', 'Type', 'CurrencyCode']]
        df_accounts.to_sql('xero_extract_accounts', self.__dbconn, if_exists='append', index=False)
        return df_accounts['AccountID'].to_list()

    def extract_invoices(self, page=None) -> List[str]:
        """
        Extract invoicess from Xero
        :return: List of invoice ids
        """
        logger.debug('extracting invoices from Xero')
        invoices = self.__xero.invoices.filter(page=page)
        logger.debug('invoices = %s', str(invoices))
        if not invoices:
            return []
        # invoices is a nested structure - so we to denormalize
        invl = []
        for inv in invoices:
            contact_id = inv['Contact']['ContactID']
            del inv['Payments']
            del inv['CreditNotes']
            del inv['Contact']
            del inv['Prepayments']
            del inv['Overpayments']
            del inv['LineItems']
            inv['ContactID'] = contact_id
            invl.append(inv)
       
        # temp
        # invl = invl[0:10]

        # retrieve lineitems by going after individual invoices. lineitems have tracking info that needs
        # to be denormalized as well
        litl = []
        lit_trackl = []
        for inv in invl:
            # Xero will throttle calls here - so keep a sleep in between
            time.sleep(1)
            inv_detailed = self.__xero.invoices.get(inv['InvoiceID'])[0]
            logger.debug('detailed invoice %s', str(inv_detailed))
            lits = inv_detailed['LineItems']
            for lit in lits:
                lit['InvoiceID'] = inv['InvoiceID']
                lit_tracks = lit['Tracking']
                for lit_track in lit_tracks:
                    lit_track['LineItemID'] = lit['LineItemID']
                    lit_trackl.append(lit_track)
                del lit['ValidationErrors']
                del lit['Tracking']
                litl.append(lit)

        invoice_ids = []
        if invl:
            df_invl = pd.DataFrame(invl)
            df_invl = df_invl[['Type', 'InvoiceID', 'InvoiceNumber', 'Reference', 'CurrencyRate', 'Date', 'Status', 'LineAmountTypes', 'Total', 'UpdatedDateUTC', 'CurrencyCode', 'ContactID']]
            df_invl.to_sql('xero_extract_invoices', self.__dbconn, if_exists='append', index=False)
            invoice_ids = df_invl['InvoiceID'].to_list()

        if litl:
            df_litl = pd.DataFrame(litl)
            df_litl = df_litl[['LineItemID', 'InvoiceID', 'Description', 'UnitAmount', 'LineAmount', 'AccountCode', 'Quantity']]
            df_litl.to_sql('xero_extract_invoice_lineitems', self.__dbconn, if_exists='append', index=False)

        if lit_trackl:
            df_lit_trackl = pd.DataFrame(lit_trackl)
            df_lit_trackl = df_lit_trackl[['Name', 'Option', 'TrackingCategoryID', 'TrackingOptionID', 'LineItemID']]
            df_lit_trackl.to_sql('xero_extract_lineitem_tracking', self.__dbconn, if_exists='append', index=False)

        return invoice_ids

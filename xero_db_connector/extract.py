"""
XeroExtractConnector(): Connection between Xero and Database
"""

import logging
from typing import List

import pandas as pd
import time
from os import path

logger = logging.getLogger('XeroExtractConnector')

class XeroExtractConnector:
    """
    - Extract Data from Xero and load to Database
    """
    def __init__(self, xero, dbconn):
        self.__dbconn = dbconn
        self.__xero = xero

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
        logger.info('extracting contacts from Xero')
        contacts = self.__xero.contacts.all()
        if not contacts:
            return []
        df_contacts = pd.DataFrame(contacts)
        df_contacts = df_contacts[['ContactID', 'Name', 'ContactStatus', 'EmailAddress', 'IsSupplier', 'IsCustomer']]
        df_contacts.to_sql('xero_extract_contacts', self.__dbconn, if_exists='append', index=False)
        return df_contacts['ContactID'].to_list()

    def extract_tracking_categories(self) -> List[str]:
        """
        Extract tracking options from Xero
        :return: List of tracking option ids
        """
        logger.info('extracting tracking from Xero')
        tracking_categories = self.__xero.trackingcategories.all()
        logger.info('tracking_categories = %s', str(tracking_categories))
        if not tracking_categories:
            return []
        # tracking categories is a nested structure - so we get two flatted ones and create two tables
        tcl = []
        tol = []
        for tc in tracking_categories:
            options = tc['Options']
            del tc['Options']
            tcl.append(tc)
            for to in options:
                to['TrackingCategoryID'] = tc['TrackingCategoryID']
                tol.append(to)
        df_tcl = pd.DataFrame(tcl)
        df_tcl = df_tcl[['TrackingCategoryID', 'Name', 'Status']]
        df_tcl.to_sql('xero_extract_tracking_categories', self.__dbconn, if_exists='append', index=False)
        df_tol = pd.DataFrame(tol)
        df_tol = df_tol[['TrackingOptionID', 'Name', 'Status', 'TrackingCategoryID']]
        df_tol.to_sql('xero_extract_tracking_options', self.__dbconn, if_exists='append', index=False)
        return df_tcl['TrackingCategoryID'].to_list()

    def extract_accounts(self) -> List[str]:
        """
        Extract accounts from Xero
        :return: List of account ids
        """
        logger.info('extracting accounts from Xero')
        accounts = self.__xero.accounts.all()
        logger.info('accounts = %s', str(accounts))
        if not accounts:
            return []
        df_accounts = pd.DataFrame(accounts)
        df_accounts = df_accounts[['AccountID', 'Code', 'Name', 'Status', 'Type', 'CurrencyCode', 'Description']]
        df_accounts.to_sql('xero_extract_accounts', self.__dbconn, if_exists='append', index=False)
        return df_accounts['AccountID'].to_list()

    def extract_invoices(self) -> List[str]:
        """
        Extract invoicess from Xero
        :return: List of invoice ids
        """
        logger.info('extracting invoices from Xero')
        invoices = self.__xero.invoices.all()
        logger.info('invoices = %s', str(invoices))
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
        invl = invl[0:10]

        # retrieve lineitems by going after individual invoices. lineitems have tracking info that needs
        # to be denormalized as well
        litl = []
        lit_trackl = []
        for inv in invl:
            time.sleep(1)
            inv_detailed = self.__xero.invoices.get(inv['InvoiceID'])[0]
            logger.info('detailed invoice %s', str(inv_detailed))
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

        df_invl = pd.DataFrame(invl)
        df_invl = df_invl[['Type', 'InvoiceID', 'InvoiceNumber', 'Reference', 'CurrencyRate', 'DateString', 'Date', 'Status', 'LineAmountTypes', 'Total', 'UpdatedDateUTC', 'CurrencyCode', 'ContactID']]
        df_invl.to_sql('xero_extract_invoices', self.__dbconn, if_exists='append', index=False)
        df_litl = pd.DataFrame(litl)
        df_litl = df_litl[['LineItemID', 'InvoiceID', 'Description', 'UnitAmount', 'LineAmount', 'AccountCode', 'Quantity']]
        df_litl.to_sql('xero_extract_invoice_lineitems', self.__dbconn, if_exists='append', index=False)
        df_lit_trackl = pd.DataFrame(lit_trackl)
        df_lit_trackl = df_lit_trackl[['Name', 'Option', 'TrackingCategoryID', 'TrackingOptionID', 'LineItemID']]
        df_lit_trackl.to_sql('xero_extract_lineitem_tracking', self.__dbconn, if_exists='append', index=False)
        return df_invl['InvoiceID'].to_list()

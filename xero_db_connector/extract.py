"""
XeroExtractConnector(): Connection between Xero and Database
"""

import logging
from typing import List

import pandas as pd
from xero import Xero
from xero.auth import PrivateCredentials

logger = logging.getLogger('XeroExtractConnector')


class XeroExtractConnector:
    """
    - Extract Data from Xero and load to Database
    """
    def __init__(self, config, connection):
        self.__connection = connection
        with open(config.get('xero_keyfile')) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(config.get('xero_consumer_key'), rsa_key)
        self.__xero = Xero(credentials)

    def get_xero(self):
        return self.__xero
    
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
        df_contacts.to_sql('xero_extract_contacts', self.__connection, if_exists='replace', index=False)
        return df_contacts['ContactID'].to_list()

    def extract_tracking_options(self) -> List[str]:
        """
        Extract tracking options from Xero
        :return: List of tracking option ids
        """
        logger.info('extracting tracking from Xero')
        tracking_categories = self.__xero.trackingcategories.all()
        logger.info('tracking_categories = %s', str(tracking_categories))
        if not tracking_categories:
            return []
        tc_flattened = []
        for trc in tracking_categories:
            for tro in trc['Options']:
                tc_entry = {
                    'TrackingCategoryName': trc['Name'],
                    'TrackingCategoryID': trc['TrackingCategoryID'],
                    'TrackingOptionID': tro['TrackingOptionID'],
                    'TrackingOptionName': tro['Name'],
                    'TrackingOptionStatus': tro['Status']
                }
                tc_flattened.append(tc_entry)
        df_tc = pd.DataFrame(tc_flattened)
        df_tc.to_sql('xero_extract_tracking_options', self.__connection, if_exists='replace', index=False)
        return df_tc['TrackingOptionID'].to_list()

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
        df_accounts.to_sql('xero_extract_accounts', self.__connection, if_exists='replace', index=False)
        return df_accounts['AccountID'].to_list()


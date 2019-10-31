"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from os import path
from typing import BinaryIO

import pandas as pd

logger = logging.getLogger('XeroLoadConnector')


class XeroLoadConnector:
    """
    - Extract Data from Database and load to Xero
    """
    def __init__(self, xero, dbconn):
        self.__xero = xero
        self.__dbconn = dbconn

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'load_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)

"""
XeroExtractConnector(): Connection between Xero and Database
"""

import logging
from typing import List

import pandas as pd

logger = logging.getLogger('XeroExtractConnector')


class XeroExtractConnector:
    """
    - Extract Data from Xero and load to Database
    """
    def __init__(self, config, database):
        self.__database = database
        self.__config = config



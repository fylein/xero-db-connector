"""
XeroLoadConnector(): Connection between Xero and Database
"""

import logging
from typing import BinaryIO

import pandas as pd

logger = logging.getLogger('XeroLoadConnector')


class XeroLoadConnector:
    """
    - Extract Data from Database and load to Xero
    """
    def __init__(self, config, database):
        self.__database = database
        self.__config = config


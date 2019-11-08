import pytest

import sqlite3
import logging
import os
from os import path
import json

logger = logging.getLogger(__name__)

def get_mock_xero_dict():
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, 'mock_xero.json')
    mock_xero_json = open(filepath, 'r').read()
    mock_xero_dict = json.loads(mock_xero_json)
    return mock_xero_dict

def dict_compare_keys(d1, d2, key_path=''):
    ''' Compare two dicts recursively and see if dict1 has any keys that dict2 does not
    Returns: list of key paths
    '''
#    logger.info('args d1=%s, d2=%s, key_path=%s', d1, d2, key_path)
    res = []
    for k in d1:
#        logger.info('enter: processing key=%s, res=%s', k, res)
        if k not in d2:
            missing_key_path = f'{key_path}->{k}'
#            logger.info('missing_key_path=%s', missing_key_path)
            res.append(missing_key_path)
#            logger.info('res=%s', res)
        elif isinstance(d1[k], dict):
            key_path = f'{key_path}->{k}'
#                logger.info('pre res=%s', str(res))
            res1 = dict_compare_keys(d1[k], d2[k], key_path)
#                logger.info('post res=%s, res1=%s', str(res), str(res1))
            res = res + res1
        elif isinstance(d1[k], list):
            key_path = f'{key_path}->[0]'
            dv1 = d1[k][0] if len(d1[k]) > 0 else {}
            dv2 = d2[k][0] if len(d2[k]) > 0 else {}
#                logger.info('pre res=%s', str(res))
            res1 = dict_compare_keys(dv1, dv2, key_path)
#                logger.info('post res=%s, res1=%s', str(res), str(res1))
            res = res + res1
#        logger.info('exit: processing key=%s, res=%s', k, res)
    return res
# Xero Database Connector
Connects Xero to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install xero-db-connector

## Usage

To use this connector you'll need Xero credentials - specifically the keyfile and consumer key. 

Here's example usage. 

```python
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector
import sqlite3
import logging
from xero import Xero
from xero.auth import PrivateCredentials

def xero_connect():
    XERO_PRIVATE_KEYFILE = os.environ.get('XERO_PRIVATE_KEYFILE', None)
    XERO_CONSUMER_KEY = os.environ.get('XERO_CONSUMER_KEY', None)
    if XERO_PRIVATE_KEYFILE is None:
        raise Exception('XERO_PRIVATE_KEYFILE is not set')
    if XERO_CONSUMER_KEY is None:
        raise Exception('XERO_CONSUMER_KEY is not set')
    with open(XERO_PRIVATE_KEYFILE) as keyfile:
        rsa_key = keyfile.read()
    credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)
    # used to connect to xero
    return Xero(credentials)

dbconn = sqlite3.connect('/tmp/xero.db')
xero = xero_connect()
x = XeroExtractConnector(xero=xero, dbconn=dbconn)
x.create_tables()
y = XeroLoadConnector(xero=xero, dbconn=dbconn)
y.create_tables()
x.extract_contacts()
x.extract_tracking_categories()
x.extract_accounts()

# do some transformations and populated invoice tables xero_load_invoices and xero_load_invoice_lineitems

x.load_invoice(invoice_id='ID1')
```

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
* Make necessary changes
* Run unit tests to ensure everything is fine

## Unit Tests

To run unit tests, run pytest in the following manner:

```
python -m pytest test/unit
```

You should see something like this:
```
================================================================== test session starts ==================================================================
platform darwin -- Python 3.7.4, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /Users/siva/src/xero-db-connector, inifile: pytest.ini
plugins: mock-1.11.2, cov-2.8.1
collected 3 items                                                                                                                                       

test/unit/test_mocks.py::test_xero_mock_setup PASSED                                                                                              [ 33%]
test/unit/test_mocks.py::test_dbconn_mock_setup PASSED                                                                                            [ 66%]
test/unit/test_mocks.py::test_xec_mock_setup PASSED                                                                                               [100%]

=================================================================== 3 passed in 0.10s ===================================================================

```

## Integration Tests

To run unit tests, you will need a mechanism to connect to a real Xero account. Specifically, you'll need a keyfile and a consumer key, both of which can be obtained from the xero developer portal. Set the following environment variables before running the integration tests:

```
export XERO_PRIVATE_KEYFILE=<path_to_keyfile>
export XERO_CONSUMER_KEY=<string>

python -m pytest test/integration
```

## Code coverage

To get code coverage report, run this command:

```python
python -m pytest --cov=xero_db_connector

<snipped output>

Name                            Stmts   Miss  Cover
---------------------------------------------------
xero_db_connector/__init__.py       0      0   100%
xero_db_connector/extract.py      106      0   100%
xero_db_connector/load.py          52      0   100%
---------------------------------------------------
TOTAL                             158      0   100%
```

To get an html report, run this command:

```python
python -m pytest --cov=xero_db_connector --cov-report html:cov_html
```

We want to maintain code coverage of more than 95% for this project at all times.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

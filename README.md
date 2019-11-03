# Xero Database Connector
Connects Xero to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install xero-db-connector

## Usage

To use this connector you'll need Xero credentials - specifically the keyfile and consumer key.

Here's example usage. Note the detect_types part - this is essential for timestamp to be translated to datetime.datetime type.


```python
from xero_db_connector.extract import XeroExtractConnector
from xero_db_connector.load import XeroLoadConnector
import sqlite3
import logging
from xero import Xero
from xero.auth import PrivateCredentials

logging.basicConfig(
    format='%(asctime)s %(name)s: %(message)s', level=logging.INFO)
dbconn = sqlite3.connect("/tmp/xero.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
xero_keyfile = 'XXX'
xero_consumer_key = 'XXX'
with open(xero_keyfile) as keyfile:
    rsa_key = keyfile.read()
credentials = PrivateCredentials(xero_consumer_key, rsa_key)
xero = Xero(credentials)
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

## Tests

To run unit tests, set the following two environment variables which will allow connection to a Xero account, preferably the demo account.

```
export XERO_PRIVATE_KEYFILE=<path_to_keyfile>
export XERO_CONSUMER_KEY=<string>
```

Then run pytest and you should see something like this.

```python
(venv) siva-laptop-2:xero-db-connector siva$ pytest

=================================================================== test session starts ====================================================================
platform darwin -- Python 3.7.4, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /Users/siva/src/xero-db-connector, inifile: pytest.ini
plugins: cov-2.8.1
collected 3 items                                                                                                                                          

test/test_xero.py::test_xero_connection PASSED                                                                                                       [ 33%]
test/test_xero.py::test_extract_accounts PASSED                                                                                                      [ 66%]
test/test_xero.py::test_extract_tracking_categories PASSED                                                                                           [100%]

```

To get code coverage report, run this command:

```python
(venv) siva-laptop-2:xero-db-connector siva$ pytest --cov=xero_db_connector

<snipped output>

---------- coverage: platform darwin, python 3.7.4-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
xero_db_connector/__init__.py       0      0   100%
xero_db_connector/extract.py      100     57    43%
xero_db_connector/load.py          42     29    31%
---------------------------------------------------
TOTAL                             142     86    39%

============================================================== 3 passed, 1 warnings in 5.08s ===============================================================
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


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

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
```

# do some magic

y.load_invoice(invoice_id='I1')
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

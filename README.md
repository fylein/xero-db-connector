# Xero Database Connector
Connects Xero to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install xero-db-connector

## Usage

To use this connector you'll need these Xero credentials.

This connector is very easy to use.
1. First you'll need to create a connection using the main class XeroSDK.

```python
from xero_db_connector.extract import XeroExtractConnector
import sqlite3
import logging
from xero import Xero
from xero.auth import PrivateCredentials

logging.basicConfig(
    format='%(asctime)s %(name)s: %(message)s', level=logging.DEBUG)
dbconn = sqlite3.connect("/tmp/xero.db")
xero_keyfile = 'XXX'
xero_consumer_key = 'XXX'
with open(xero_keyfile) as keyfile:
    rsa_key = keyfile.read()
credentials = PrivateCredentials(xero_consumer_key, rsa_key)
xero = Xero(credentials)
x = XeroExtractConnector(xero=xero, dbconn=dbconn)
x.create_tables()
x.extract_invoices()
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

# Xero Database Connector
Connects Xero to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install xero-db-connector

## Usage

To use this connector you'll need these Xero credentials used for OAuth2 authentication: **client ID**, **client secret** and **refresh token**.

This connector is very easy to use.
1. First you'll need to create a connection using the main class XeroSDK.
```python
from xero_db_connector import XeroExtractConnector

config = {
    'xero_base_url': '<YOUR BASE URL>',
    'xero_client_id': '<YOUR CLIENT ID>',
    'xero_client_secret': '<YOUR CLIENT SECRET>',
    'xero_refresh_token': '<YOUR REFRESH TOKEN>' 
}

extract_connector = XeroExtractConnector(
    config, database_connector
)
```
2. After that you'll be able to extract data from xero and store it in the db
```python
# Extract Expenses
extract_connector.extract_expenses()

#Extract Employees
extract_connector.extract_employees()
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

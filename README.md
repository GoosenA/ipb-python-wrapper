# ipb_client
Python wrapper for Investec Programmable Banking



# Investec Open API 
This package is a wrapper for the Investec OpenAPI. More information on the API is available [here](https://developer.investec.com/za/home). 


## Prerequisites
* Python 3.7 or later

## Installation

Requires python 3.7 or above. Available via pypi package manager 
```shell
pip install investec-openapi-wrapper
```

## Usage

### Authorization
The Account Information and Programmable Card API endpoints are protected by the OAuth 2.0 Authorization Framework. More information is available [here](https://developer.investec.com/za/home)

```python
from personal_banking_client import PersonalBankingClient
client = PersonalBankingClient(credentials_path=file_path)
```

where the credentials file looks as follows:
```json
{
    "client_id": "test", 
    "secret": "test"
}
```

### Personal Banking Client
The Account Information API allows Investec SA Private Banking clients to access their account and transactional information (read-only) via an API. More information is available [here](https://developer.investec.com/za/home)


#### get_accounts
Lists all the users accounts.

```python
accounts = client.get_accounts()
```
Example Response
```json
{"accounts": 
    [{
        "accountId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
        "accountNumber": "xxxxxxxxxxx", 
        "accountName": "Mrs J Smith", 
        "referenceName": "Investec (Main)", 
        "productName": "Private Bank Account", 
        "kycCompliant": True, 
        "profileId": "xxxxxxxxxxxxxx"
    }]
}
```


#### get_account_balance
Get the current balance for the specified account

```python
balance = client.get_account_balance('account_id')
```
Example Response
```json
{
    "accountId": "xxxxxxxxxxxxxxxxxxxxxxxxx", 
    "currentBalance": 1000.00, 
    "availableBalance": 11000.00, 
    "currency": "ZAR"
}
```

#### get_account_transactions
Lists all transactions for a specified account. Optional additional fields allow the user to specify a date range to filter transactions for. 

```python
transactions = client.get_account_transactions('account_id')

start_date = datetime.today()-timedelta(days=1)
end_date = datetime.today()
transactions = client.get_account_transactions('account_id', from_date = start_date)
transactions = client.get_account_transactions('account_id', to_date = end_date)
transactions = client.get_account_transactions('account_id', from_date = start_date, to_date=end_date)
```
Example Response
```json
{"transactions": 
    [
        {
            "accountId": "xxxxxxxxxxxxxxxxxxxxxxxxxx", 
            "type": "CREDIT", 
            "transactionType": None, 
            "status": "POSTED", 
            "description": "Interest Value Date 01Jan23", 
            "cardNumber": "", 
            "postedOrder": 0, 
            "postingDate": "2023-01-03", 
            "valueDate": None, 
            "actionDate": "2023-01-01", 
            "transactionDate": "2023-01-01", 
            "amount": 100.00, 
            "runningBalance": 11000.00
        }  
    ]
}
```

#### transfer_multiple
Transfer funds between two internal accounts. The account IDs can be retrieved using the get_accounts function.

```python
transfer_details = [{
        "beneficiaryAccountId": "destination account ID",
        "amount": "1.01", # in Rand
        "myReference": "Reference for source account",
        "theirReference": "Reference for destination account"
}]
response = client.transfer_multiple('account_id', transfer_details)
```

#### pay_multiple
Pay multiple benificiaries. Benificiary details can be retrieved using the get_beneficiaries function.

```python
payments_details = [{
        "beneficiaryId": "Beneficiary ID",
        "amount": "1.01", # in Rand
        "myReference": "Reference for source account",
        "theirReference": "Reference for beneficiary"
}]
response = client.pay_multiple()
```


#### get_beneficiaries
Get a list of beneficiaries.

```python
beneficiaries = client.get_beneficiaries()
```

Example result:
```json
[{
    "beneficiaryId": "xxxxxxxxxxxxxxxxxxx", 
    "accountNumber": "xxxxxxxxxx", 
    "code": "xxxxxx", 
    "bank": "Some bank", 
    "beneficiaryName": "Some beneficiary", 
    "lastPaymentAmount": "500.00", 
    "lastPaymentDate": "21/03/2023", 
    "cellNo": 00000000000, 
    "emailAddress": "test@email.com", 
    "name": "Some beneficiary", 
    "referenceAccountNumber": "Their reference", 
    "referenceName": "My reference", 
    "categoryId": "xxxxxxxxxxxxxx", 
    "profileId": "xxxxxxxxxxxxxx"
}]
```


#### get_beneficiary_categories
Get a list of configured beneficiary categories. 

```python
beneficiary_categories = client.get_beneficiary_categories()
```
Example Result
```json
[{
    "id": "xxxxxxxxxxxxxx", 
    "isDefault": "true", 
    "name": "Not Categorised"    
}]
```

## Build pypi package

```shell
python -m build
python -m twine upload dist/*
```
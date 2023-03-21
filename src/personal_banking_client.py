from datetime import datetime
from client import Client

import requests
import json
import os


class PersonalBankingClient(Client):
    def __init__(self, client_id: str = None, secret: str = None, credentials_path=""):
        """Create a client instance with the provided options."""
        if not client_id or not secret:
            try:
                credentials = json.load(open(os.path.expanduser(credentials_path)))
                client_id = credentials.get("client_id", None)
                secret = credentials.get("secret", None)
            except:
                raise ValueError("ClientID and Secret not specified")

        super().__init__(client_id, secret)

        self.base = "za/pb/v1"

    def get_accounts(self) -> dict:
        url = f"{self.host}/{self.base}/accounts"
        try:
            response = requests.get(
                url=url, headers=self._bearer_header(), auth=self.authorization_bearer
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                # if "data" in content:
                #     return content["data"]
                return content

    def get_account_balance(self, account_id: str) -> dict:
        """Gets the balance for an account."""

        url = f"{self.host}/{self.base}/accounts/{account_id}/balance"
        try:
            response = requests.get(
                url=url, headers=self._bearer_header(), auth=self.authorization_bearer
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                # if "data" in content:
                #     return content["data"]
                return content

    def get_account_transactions(
        self,
        account_id: str,
        from_date: datetime = None,
        to_date: datetime = None,
        transaction_type: str = None,
    ) -> dict:
        """Gets the transactions for an account."""
        if from_date and to_date and to_date < from_date:
            raise ValueError("The from_date must be before the to_date")

        params = {}
        if from_date:
            params["fromDate"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["toDate"] = to_date.strftime("%Y-%m-%d")
        if transaction_type:
            params["transactionType"] = transaction_type

        url = f"{self.host}/{self.base}/accounts/{account_id}/transactions"
        try:
            response = requests.get(
                url=url,
                headers=self._bearer_header(),
                params=params,
                auth=self.authorization_bearer,
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                # if "data" in content:
                #     return content["data"]
                return content

    def transfer_multiple(self, account_id, transfer_details=[]):
        """
        account_id = From where to transfer

        transfer_details = [{
                "beneficiaryAccountId": Where to transfer to,
                "amount": "1.01" - Rands,
                "myReference": Reference for source account,
                "theirReference": Reference for destination account
        }]
        """
        body = {"TransferList": transfer_details}
        headers = {
            "Content-Type": "application/json",
        }

        url = f"{self.host}/{self.base}/accounts/{account_id}/transfermultiple"
        response = requests.post(
            url,
            json=body,
            headers=headers,
            auth=self.authorization_bearer,
            timeout=self.timeout,
        )

        return response

    def pay_multiple(self, account_id, payment_details=[]):
        """
        account_id = From where to make payment

        payment_details = [{
                "beneficiaryId": Where to make payment to,
                "amount": "1.01" - Rands,
                "myReference": Reference for source account,
                "theirReference": Reference for destination account
        }]
        """
        body = {"paymentList": payment_details}
        headers = {
            "Content-Type": "application/json",
        }

        url = f"{self.host}/{self.base}/accounts/{account_id}/paymultiple"
        response = requests.post(
            url,
            json=body,
            headers=headers,
            auth=self.authorization_bearer,
            timeout=self.timeout,
        )

        return response

    def get_beneficiaries(self) -> dict:
        """Gets beneficiaries"""

        url = f"{self.host}/{self.base}/accounts/beneficiaries"
        try:
            response = requests.get(
                url=url, headers=self._bearer_header(), auth=self.authorization_bearer
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                # if "data" in content:
                #     return content["data"]
                return content

    def get_beneficiary_categories(self) -> dict:
        """Gets beneficiary categories"""

        url = f"{self.host}/{self.base}/accounts/beneficiarycategories"
        try:
            response = requests.get(
                url=url, headers=self._bearer_header(), auth=self.authorization_bearer
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                return content

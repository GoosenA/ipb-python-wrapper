from datetime import datetime
from authorization_bearer import AuthorizationBearer
from client import Client

import requests
import json
import os


class OpenAPIClient(Client):
    def __init__(self, client_id: str=None, secret: str=None, credentials_path=""):
        """ Create a client instance with the provided options."""
        if not client_id or not secret:
            try:
                credentials = json.load(open(os.path.expanduser(credentials_path)))
                client_id = credentials.get("client_id", None)
                secret = credentials.get("secret", None)
            except:
                print("ClientID and Secret not specified")
                return
        super().__init__(client_id, secret)

        self.base = f"za/pb/v1"

    def get_accounts(self) -> dict:
        url = f"{self.host}/{self.base}/accounts"
        try:
            response = self.get(
                url=url,
                headers=self._bearer_header()
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                if "data" in content:
                    return content["data"]
                return content

    def get_transactions(self, account_id: str, from_date: datetime=None, to_date: datetime=None) -> dict:
        """ Gets the transactions for an account."""
        if from_date and to_date and to_date < from_date:
            raise ValueError("The from_date must be before the to_date")

        params = {}
        if from_date:
            params["fromDate"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["toDate"] = to_date.strftime("%Y-%m-%d")

        url = f"{self.host}/{self.base}/accounts/{account_id}/transactions"
        try:
            response = self.get(
                url=url,
                headers=self._bearer_header()
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                if "data" in content:
                    return content["data"]
                return content

    def get_balance(self, account_id: str) -> dict:
        """ Gets the balance for an account."""

        url = f"{self.host}/{self.base}/accounts/{account_id}/balance"
        try:
            response = self.get(
                url=url,
                headers=self._bearer_header()
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                content = json.loads(response.text)
                if "data" in content:
                    return content["data"]
                return content

    def make_inter_account_transfer(self, source_account_id, transfer_details = []):
        """
        source_account_id = From where to transfer
        
        transfer_details = [{
                "BeneficiaryAccountId": Where to transfer to,
                "Amount": "1.01" - Rands,
                "MyReference": Reference for source account,
                "TheirReference": Reference for destination account
        }]
        """
        body = {
            "AccountId": source_account_id,
            "TransferList": transfer_details
        }
        headers = {
            "Content-Type": "application/json",
        }

        url = f"{self.host}/{self.base}/accounts/transfermultiple"
        auth = AuthorizationBearer(self.access_token)
        response = requests.post(url, json=body, headers=headers, auth=auth, timeout=self.timeout)

        return response


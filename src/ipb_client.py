from datetime import datetime, timedelta
from requests import auth

import requests
import json
import os



class AuthorizationBearer(requests.auth.AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class OpenAPIClient():
    """
    >>> client = investec.Client("Your Client ID", "Your Secret")
    """

    def __init__(self, client_id: str=None, secret: str=None, timeout: int=30, credentials_path=""):
        """ Create a client instance with the provided options."""
        if not client_id or not secret:
            credentials = json.load(open(os.path.expanduser(credentials_path)))
            client_id = credentials.get("client_id", None)
            secret = credentials.get("secret", None)

        self.client_id = client_id
        self.secret = secret
        self.timeout = timeout
        self.requests_session = requests.Session()
        self.api_host = "https://openapi.investec.com"
        self.token_expires = datetime.now()
        self.token = None
    
    def api_call(self, service_url: str, method: str="get", params: dict=None, body: str=None) -> dict:
        """ Helper function to create calls to the API."""

        if not self.token or datetime.now() >= self.token_expires:
            self.get_access_token() # Need to get a new token

        request = getattr(self.requests_session, method)
        headers = {"Accept": "application/json"}
        if method == "post":
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
        auth = AuthorizationBearer(self.token)

        response = request(f"{self.api_host}/{service_url}", params=params, data=body, headers=headers, auth=auth, timeout=self.timeout)
        try:
            response.raise_for_status()
            content = response.json()
            if "data" in content:
                return content["data"]
            return content
        except:
            raise requests.exceptions.HTTPError(response.status_code, response.content)

    def get_access_token(self) -> None:
        """ Get an access token."""

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "openapi.investec.com",
        }

        body = {
            "grant_type":"client_credentials",
            "scope":"accounts"
        }

        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret)
        
        url = f"{self.api_host}/identity/v2/oauth2/token"
        response = requests.post(url, data=body, headers=headers, auth=auth, timeout=self.timeout).json()

        self.token = response["access_token"]
        token_expiry = response["expires_in"] - 60 
        self.token_expires = datetime.now() + timedelta(seconds=token_expiry)

    def get_accounts(self) -> dict:
        """ Gets the available accounts."""
        url = f"/za/pb/v1/accounts"
        return self.api_call(url)

    def get_transactions(self, account_id: str, from_date: datetime=None, to_date: datetime=None) -> dict:
        """ Gets the transactions for an account."""
        if from_date and to_date and to_date < from_date:
            raise ValueError("The from_date must be before the to_date")

        params = {}
        if from_date:
            params["fromDate"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["toDate"] = to_date.strftime("%Y-%m-%d")

        url = f"/za/pb/v1/accounts/{account_id}/transactions"
        return self.api_call(url, params=params)

    def get_balance(self, account_id: str) -> dict:
        """ Gets the balance for an account."""
        url = f"/za/pb/v1/accounts/{account_id}/balance"
        return self.api_call(url)

    def make_inter_account_transfer(self, source_account_id, transfer_details = []):
        """
        source_account_id = From where to transfer
        
        transfer_details = [{
                "BeneficiaryAccountId": destination_account_id,
                "Amount": "1.01",
                "MyReference": "Test from PBA to PS",
                "TheirReference": "Test1"
        }]
        """
        body = {
            "AccountId": source_account_id,
            "TransferList": transfer_details
        }

        headers = {
            "Content-Type": "application/json",
        }

        url = f"{self.api_host}/za/pb/v1/accounts/transfermultiple"
        auth = AuthorizationBearer(self.token)
        

        response = requests.post(url, data=body, headers=headers, auth=auth, timeout=self.timeout)
        return response


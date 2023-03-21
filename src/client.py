import requests
import json

from datetime import datetime, timedelta


class AuthorizationBearer(requests.auth.AuthBase):
    """Authorization bearer class"""

    def __init__(self, access_token):
        """Create authorization bearer instance."""
        self.access_token = access_token

    def __call__(self, request):
        """Create request header using authorization bearer"""
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class Client:
    """Client class"""

    def __init__(self, client_id: str = None, secret: str = None, timeout: int = 30):
        """Create a client instance with the provided options."""
        if not client_id or not secret:
            raise ValueError("ClientID and secret not specified")

        self.client_id = client_id
        self.secret = secret

        self._basic_auth_token = requests.auth.HTTPBasicAuth(
            self.client_id, self.secret
        )
        self._basic_auth_token_expires = datetime.now()
        self.timeout = timeout

        self._access_token = None
        self._expires_in = None  # lifetime in seconds, 3600 == 1 hour.

        self._host = "https://openapi.investec.com"
        self._domain = "identity"
        self._version = "v2"
        self.auth_url = None

        self._authentication()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def basic_auth_token(self):
        return self._basic_auth_token

    @property
    def basic_auth_token_expires(self):
        return self._basic_auth_token_expires

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, value):
        if value is not None:
            self._expires_in = value
            self._basic_auth_token_expires = datetime.now()
            +timedelta(seconds=value)

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def authorization_bearer(self):
        return self._authorization_bearer

    @authorization_bearer.setter
    def authorization_bearer(self, value):
        self._authorization_bearer = value

    @staticmethod
    def _basic_header():
        return {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "openapi.investec.com",
        }

    @staticmethod
    def _bearer_header():
        return {
            "content-type": "application/json",
        }

    def _authentication(self):
        """
        Does oauth2 authentication,
        uses the token as the initial Basic auth api key.
        """
        if self.basic_auth_token_expires - timedelta(seconds=30) > datetime.now():
            return

        if self.auth_url is None:
            self.auth_url = f"{self._host}/{self._domain}/{self._version}/oauth2/token"

        response = requests.post(
            url=self.auth_url,
            headers=self._basic_header(),
            auth=self.basic_auth_token,
            data={"grant_type": "client_credentials", "scope": "accounts"},
        )
        self.access_token = json.loads(response.text).get("access_token")
        self.expires_in = response.json().get("expires_in")

        self.authorization_bearer = AuthorizationBearer(self._access_token)

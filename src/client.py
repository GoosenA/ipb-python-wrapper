import requests
import json

from datetime import datetime, timedelta
from authorization_bearer import AuthorizationBearer


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]



class Client(metaclass=Singleton):
    def __init__(self, client_id: str=None, secret: str=None, timeout: int=30):
        """ Create a client instance with the provided options."""
        if not client_id or not secret:
            raise ValueError("ClientID and secret not specified")

        self.client_id = client_id
        self.secret = secret

        self._basic_auth_token = requests.auth.HTTPBasicAuth(self.client_id, self.secret)
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

    # @basic_auth_token.setter
    # def basic_auth_token(self, value):
    #     self._basic_auth_token = value

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
            self._basic_auth_token_expires = datetime.now() + timedelta(seconds=value)

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

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
        """Does oauth2 authentication, uses the token as the initial Basic auth api key."""
        if self.basic_auth_token_expires - timedelta(seconds=30) > datetime.now():
            return

        if self.auth_url is None:
            self.auth_url = f"{self._host}/{self._domain}/{self._version}/oauth2/token"

        response = self.post(
            url=self.auth_url,
            headers=self._basic_header(),
            authorization=self.basic_auth_token,
            body = {
                "grant_type":"client_credentials",
                "scope":"accounts"
            }
        )

        self.access_token = json.loads(response.text).get("access_token")  # have a none base exception.
        self.expires_in = response.json().get("expires_in")

    @staticmethod
    def post(url, headers, authorization, body):
        """Make a post request."""

        return requests.post(
            url=url,
            headers=headers,
            data=body,
            auth=authorization,
        )

    def get(self, url, headers):
        """Make a get request."""
        self._authentication()

        return requests.get(
            url=url,
            headers=headers,
            auth=AuthorizationBearer(self._access_token)
        )
    
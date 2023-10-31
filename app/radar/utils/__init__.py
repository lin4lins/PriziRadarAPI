import requests
from rest_framework.exceptions import AuthenticationFailed

GRAPH_API_VERSION = "v17.0"
FACEBOOK_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
ACCOUNTS_URL = f"{FACEBOOK_API_BASE_URL}/me/accounts"
QUERY_HASH = "eaffee8f3c9c089c9904a5915a898814"


ERROR_TYPES = {"OAuthException": AuthenticationFailed()}


def build_url(base_url, params):
    """Build a URL with parameters."""
    param_string = '&'.join(
        [f'{key}={value}' for key, value in params.items()])
    return f"{base_url}?{param_string}"


def make_request(url):
    """Make an HTTP GET request and return the JSON response."""
    response = requests.get(url)
    if response.status_code != 200:
        error_type = response.json()['error']['type']
        raise ERROR_TYPES[error_type]

    return response.json()


class Base:
    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}

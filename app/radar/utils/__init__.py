import requests
from rest_framework.exceptions import NotFound

GRAPH_API_VERSION = "v17.0"
FACEBOOK_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
ACCOUNTS_URL = f"{FACEBOOK_API_BASE_URL}/me/accounts"
QUERY_HASH = "eaffee8f3c9c089c9904a5915a898814"


def build_url(base_url, params):
    """Build a URL with parameters."""
    param_string = '&'.join(
        [f'{key}={value}' for key, value in params.items()])
    return f"{base_url}?{param_string}"


def make_request(url):
    """Make an HTTP GET request and return the JSON response."""
    response = requests.get(url)
    if response.status_code != 200:
        raise NotFound(response.json())
    return response.json()
import requests

GRAPH_API_VERSION = "v17.0"
FACEBOOK_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
ACCOUNTS_URL = f"{FACEBOOK_API_BASE_URL}/me/accounts"
QUERY_HASH = "eaffee8f3c9c089c9904a5915a898814"


# Genaral
def build_url(base_url, params):
    """Build a URL with parameters."""
    param_string = '&'.join(
        [f'{key}={value}' for key, value in params.items()])
    return f"{base_url}?{param_string}"


def make_request(url):
    """Make an HTTP GET request and return the JSON response."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# Urls generation
def get_ig_business_accounts_url(access_token: str) -> str:
    """Generate Instagram business accounts URL."""
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    return build_url(ACCOUNTS_URL, params)


def generate_instagram_media_url(account_ig_id: str, access_token: str) -> str:
    """Generate Instagram media URL for a specific account."""
    params = {"fields": "ig_id", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_ig_id}/media", params)




def get_account_ig_id(access_token: str) -> str:
    """Get Instagram business account ID."""
    data = make_request(get_ig_business_accounts_url(access_token))
    return data["data"][0]["instagram_business_account"]["id"]


def get_post_old_ig_id(shortcode: str) -> str:
    """Get old Instagram media ID."""
    url = f'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables={{"shortcode": "{shortcode}"}}'
    data = make_request(url)
    return data['data']['shortcode_media']['id']


def get_post_ig_id(account_ig_id: str, shortcode: str,
                   access_token: str) -> str:
    """Get new post ID by old version ID."""
    old_version_id = get_post_old_ig_id(shortcode)
    data = make_request(
        generate_instagram_media_url(account_ig_id, access_token))
    for post in data['data']:
        if post['ig_id'] == old_version_id:
            return post['id']

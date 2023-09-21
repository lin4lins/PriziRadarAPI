import requests

GRAPH_API_VERSION = "v17.0"
FACEBOOK_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
ACCOUNTS_URL = f"{FACEBOOK_API_BASE_URL}/me/accounts"
QUERY_HASH = "eaffee8f3c9c089c9904a5915a898814"


def build_url(base_url, params):
    """Build a URL with parameters."""
    param_string = '&'.join([f'{key}={value}' for key, value in params.items()])
    return f"{base_url}?{param_string}"


def get_ig_business_accounts_url(user_ig_token: str) -> str:
    """Generate the Instagram business accounts URL."""
    params = {
        "fields": "instagram_business_account",
        "access_token": user_ig_token,
    }
    return build_url(ACCOUNTS_URL, params)


def generate_instagram_media_url(user_ig_token: str, ig_account_id: str) -> str:
    instagram_media_url = f"{FACEBOOK_API_BASE_URL}/{ig_account_id}/media"
    """Generate the Instagram media URL for a specific account."""
    params = {
        "fields": "ig_id",
        "access_token": user_ig_token
    }
    return build_url(instagram_media_url, params)


def get_ig_account_id(access_token: str) -> str:
    """Get the Instagram business account ID."""
    response = requests.get(get_ig_business_accounts_url(access_token))
    response.raise_for_status()
    data_dict = response.json()
    return data_dict["data"][0]["instagram_business_account"]["id"]


def get_post_old_ig_id(shortcode: str) -> str:
    """Get the old Instagram media ID."""
    url = f'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables={{"shortcode": "{shortcode}"}}'
    response = requests.get(url)
    response.raise_for_status()
    data_dict = response.json()
    return data_dict['data']['shortcode_media']['id']


def get_post_ig_id(ig_account_id: str, access_token: str, shortcode: str) -> str:
    """Get the new post ID by old version ID."""
    old_version_id = get_post_old_ig_id(shortcode)
    url = generate_instagram_media_url(access_token, ig_account_id)
    response = requests.get(url)
    print(response.content)
    response.raise_for_status()
    data_dict = response.json()
    for post in data_dict['data']:
        if post['ig_id'] == old_version_id:
            return post['id']

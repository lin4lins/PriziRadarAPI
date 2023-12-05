from radar.utils import build_url, ACCOUNTS_URL, FACEBOOK_API_BASE_URL, make_request


def get_ig_business_account_url(access_token: str) -> str:
    """Generate Instagram business accounts URL."""
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    return build_url(ACCOUNTS_URL, params)


def generate_me_details_url(account_id: str, access_token: str) -> str:
    params = {"fields": "username,profile_picture_url", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}", params)


def generate_business_discovery_url(username: str, account_id: str, access_token: str) -> str:
    params = {"fields": f"business_discovery.username({username})", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}", params)


def get_account_id(access_token: str) -> str:
    """Get Instagram business account ID."""
    data = make_request(get_ig_business_account_url(access_token))
    print(data)
    return data["data"][0]["instagram_business_account"]["id"]


def get_account_details(account_id: str, access_token: str) -> dict:
    return make_request(generate_me_details_url(account_id, access_token))


def get_user_id_by_username(username: str, account_id: str, access_token) -> str:
    """Get Instagram business account ID."""
    data = make_request(generate_business_discovery_url(username, account_id, access_token))
    return data['business_discovery']['id']

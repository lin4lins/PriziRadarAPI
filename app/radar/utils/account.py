from radar.utils import build_url, ACCOUNTS_URL, FACEBOOK_API_BASE_URL, make_request


def get_ig_business_account_url(access_token: str) -> str:
    """Generate Instagram business accounts URL."""
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    return build_url(ACCOUNTS_URL, params)


def generate_me_details_url(account_id: str, access_token: str) -> str:
    params = {"fields": "name,username,profile_picture_url", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}", params)


def get_account_id(access_token: str) -> str:
    """Get Instagram business account ID."""
    data = make_request(get_ig_business_account_url(access_token))
    return data["data"][0]["instagram_business_account"]["id"]


def get_account_details(account_id: str, access_token: str) -> dict:
    return make_request(generate_me_details_url(account_id, access_token))


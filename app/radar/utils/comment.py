from radar.utils import build_url, FACEBOOK_API_BASE_URL, make_request, QUERY_HASH


def generate_me_media_url(account_id: str, access_token: str) -> str:
    """Generate Instagram media URL for a specific account."""
    params = {"fields": "ig_id", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}/media", params)


def generate_post_comments_url(post_ig_id: str, access_token: str) -> str:
    """Generate Instagram comments URL for a specific post."""
    params = {"fields": "text,username", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{post_ig_id}/comments", params)


def generate_business_discovery_url(username: str, account_id: str, access_token: str) -> str:
    params = {"fields": f"business_discovery.username({username})", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}", params)


def get_post_old_ig_id(shortcode: str) -> str:
    """Get old Instagram media ID."""
    url = f'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables={{"shortcode": "{shortcode}"}}'
    data = make_request(url)
    return data['data']['shortcode_media']['id']


def get_post_ig_id(account_id: str, shortcode: str,
                   access_token: str) -> str:
    """Get new post ID by old version ID."""
    old_version_id = get_post_old_ig_id(shortcode)
    data = make_request(
        generate_me_media_url(account_id, access_token))
    for post in data['data']:
        if post['ig_id'] == old_version_id:
            return post['id']


def get_comments_by_post_instance(post: str, ig_account) -> list:
    """Get comments of the post by IG ID."""
    data = make_request(
        generate_post_comments_url(post.ig_id, ig_account.access_token))
    return [{
        "ig_post": post,
        "text": comment.get("text", ""),
        "author_ig_id": get_user_id_by_username(comment.get("username", ""), ig_account.ig_id, ig_account.access_token)
    } for comment in data.get("data", [])]


def get_user_id_by_username(username: str, account_id: str, access_token) -> str:
    """Get Instagram business account ID."""
    data = make_request(generate_business_discovery_url(username, account_id, access_token))
    return data['business_discovery']['id']
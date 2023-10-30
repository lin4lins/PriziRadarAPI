from urllib.parse import urlparse

from rest_framework.exceptions import ValidationError

from radar.utils import build_url, FACEBOOK_API_BASE_URL, make_request, QUERY_HASH


def generate_me_media_url(account_id: str, access_token: str) -> str:
    """Generate Instagram media URL for a specific account."""
    params = {"fields": "ig_id", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{account_id}/media", params)


def generate_post_comments_url(post_ig_id: str, access_token: str) -> str:
    """Generate Instagram comments URL for a specific post."""
    params = {"fields": "text,username", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{post_ig_id}/comments", params)


def generate_post_details_url(post_ig_id: str, access_token: str) -> str:
    params = {"fields": "id,media_type,thumbnail_url,media_url,caption,comments_count", "access_token": access_token}
    return build_url(f"{FACEBOOK_API_BASE_URL}/{post_ig_id}", params)


def get_post_old_ig_id(shortcode: str) -> str:
    """Get old Instagram media ID."""
    url = f'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}&variables={{"shortcode": "{shortcode}"}}'
    data = make_request(url)
    try:
        return data['data']['shortcode_media']['id']
    except TypeError:
        raise ValidationError("Invalid url.")


def get_post_ig_id(account_id: str, shortcode: str,
                   access_token: str) -> str:
    """Get new post ID by old version ID."""
    old_version_id = get_post_old_ig_id(shortcode)
    data = make_request(
        generate_me_media_url(account_id, access_token))
    for post in data['data']:
        if post['ig_id'] == old_version_id:
            return post['id']


def parse_shortcode(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_parts = path.split('/')
    return path_parts[-2]


def get_post_details(account_id, post_url, access_token) -> dict:
    post_shortcode = parse_shortcode(post_url)
    post_id = get_post_ig_id(account_id, post_shortcode, access_token)
    details = make_request(generate_post_details_url(post_id, access_token))
    post_type = details.pop('media_type')
    if post_type == "VIDEO":
        details['media_url'] = details.pop('thumbnail_url')

    return details

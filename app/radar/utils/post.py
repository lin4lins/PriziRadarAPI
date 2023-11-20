from urllib.parse import urlparse

from radar.utils import (FACEBOOK_API_BASE_URL, QUERY_HASH, Base, build_url,
                         make_request)


class Post(Base):
    def __init__(self, id: str, media_url: str, comments_count: str, caption: str = ""):
        self.id = id
        self.caption = caption
        self.media_url = media_url
        self.comments_count = comments_count


class IGPostFetcher:
    def __init__(self, account_id: str, access_token: str, url = None):
        self.__account_id = account_id
        self.__access_token = access_token
        self.__url = url

        self.__shortcode = None

    def __generate_media_url(self):
        params = {"fields": "ig_id", "access_token": self.__access_token}
        return build_url(f"{FACEBOOK_API_BASE_URL}/{self.__account_id}/media", params)

    def __generate_details_url(self, post_ig_id):
        params = {"fields": "id,media_type,thumbnail_url,media_url,caption,comments_count",
                  "access_token": self.__access_token}
        return build_url(f"{FACEBOOK_API_BASE_URL}/{post_ig_id}", params)

    def __get_old_ig_id(self):
        url = (f'https://www.instagram.com/graphql/query/?query_hash={QUERY_HASH}'
               f'&variables={{"shortcode": "{self.__shortcode}"}}')
        data = make_request(url)
        return data['data']['shortcode_media']['id']

    def __get_ig_id(self):
        old_version_id = self.__get_old_ig_id()
        data = make_request(self.__generate_media_url())
        for post in data['data']:
            if post['ig_id'] == old_version_id:
                return post['id']

    def __define_shortcode(self):
        parsed_url = urlparse(self.__url)
        path = parsed_url.path
        path_parts = path.split('/')
        self.__shortcode = path_parts[-2]

    def get_post(self):
        self.__define_shortcode()
        post_id = self.__get_ig_id()
        details = make_request(self.__generate_details_url(post_id))
        post_type = details.pop('media_type')
        if post_type == "VIDEO":
            details['media_url'] = details.pop('thumbnail_url')

        return Post(**details)

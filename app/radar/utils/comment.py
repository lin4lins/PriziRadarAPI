import random

from radar.utils import FACEBOOK_API_BASE_URL, Base, build_url, make_request


class Comment(Base):
    def __init__(self, author_username: str, author_avatar_url: str, text: str):
        self.author_username = author_username
        self.author_avatar_url = author_avatar_url
        self.text = text


class IGCommentFetcher:
    def __init__(self, post_id: str, access_token: str, account_id: str):
        self.__post_id = post_id
        self.__access_token = access_token
        self.__account_id = account_id

    def __generate_comments_url(self):
        params = {"fields": "id,from,text", "access_token": self.__access_token}
        return build_url(f"{FACEBOOK_API_BASE_URL}/{self.__post_id}/comments", params)

    def get_comments(self):
        comments = []
        data = make_request(self.__generate_comments_url())['data']
        for comment in data:
            author_username = comment['from']['username']
            comment_obj = Comment(author_username=author_username,
                                  author_avatar_url="dummy", text=comment['text'])
            comments.append(comment_obj)

        return comments

    def get_random_comments(self, comments_count: int):
        count = int(comments_count)
        all_comments = self.get_comments()
        return random.sample(all_comments, count)

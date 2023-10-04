import os

from dotenv import load_dotenv
from rest_framework.authtoken.models import Token

from radar.models import User, InstagramAccount

load_dotenv()

USER_DATA = {
    'email': 'user1@example.com',
    'password': 'password123'
}
IG_ACCESS_TOKEN_1 = os.getenv("IG_ACCESS_TOKEN_1")
IG_ACCESS_TOKEN_2 = os.getenv("IG_ACCESS_TOKEN_2")
IG_ID = os.getenv("IG_ID")
POST_URL = os.getenv("POST_URL")
POST_NO_COMMENTS_URL = os.getenv("POST_NO_COMMENTS_URL")
POST_SHORTCODE = os.getenv("POST_SHORTCODE")
POST_ID = os.getenv("POST_ID")
ACCOUNT_DATA_1 = {'access_token': IG_ACCESS_TOKEN_1}
ACCOUNT_DATA_2 = {'access_token': IG_ACCESS_TOKEN_2}


def authenticate(func):
    def wrapper(self, *args, **kwargs):
        user_1 = User.objects.create(**USER_DATA)
        token = Token.objects.create(user = user_1)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
        func(self, user_1, *args, **kwargs)
        self.client.credentials()
        user_1.delete()
    return wrapper


def init_ig_account(func):
    def wrapper(self, *args, **kwargs):
        user = User.objects.get(email=USER_DATA['email'])
        ig_account = InstagramAccount.objects.create(**ACCOUNT_DATA_1, user=user)
        func(self, *args, **kwargs)
        ig_account.delete()
    return wrapper


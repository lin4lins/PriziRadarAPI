import os

from dotenv import load_dotenv
from rest_framework.authtoken.models import Token

from radar.models import User

load_dotenv()

USER_DATA = {
    'email': 'user1@example.com',
    'password': 'password123'
}


def authenticate(func):
    def wrapper(self, *args, **kwargs):
        user_1 = User.objects.create(**USER_DATA)
        token = Token.objects.create(user = user_1)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token.key)
        func(self, user_1, *args, **kwargs)
        self.client.credentials()
        user_1.delete()
    return wrapper

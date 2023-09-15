from django.db import models

import requests
from rest_framework.exceptions import AuthenticationFailed

from logging_conf import logger
from radar.utils import get_facebook_accounts_url


class UserManager(models.Manager):
    @staticmethod
    def get_user_ig_id(ig_token: str) -> str:
        instagram_account_url = get_facebook_accounts_url(ig_token)
        response = requests.get(instagram_account_url)
        if response.status_code != 200:
            logger.error(f"User instagram account receiving failed. {response.content=}")
            raise AuthenticationFailed()

        id = response.json().get('data')[0].get('instagram_business_account').get('id')
        return id

    def get_or_create_with_ig_token(self, ig_token: str):
        ig_id = self.get_user_ig_id(ig_token)
        user, created = super().get_or_create(ig_id = ig_id)
        user.ig_token = ig_token
        user.save()
        return user, created


class User(models.Model):
    ig_id = models.CharField(unique=True)
    ig_token = models.CharField()
    last_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f"User {self.ig_id}, modified {self.last_modified}"

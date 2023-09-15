import requests

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed

from logging_conf import logger
from radar.utils import get_facebook_accounts_url


class InstagramAccountManager(models.Manager):
    @staticmethod
    def get_account_id(ig_token: str) -> str:
        instagram_account_url = get_facebook_accounts_url(ig_token)
        response = requests.get(instagram_account_url)
        if response.status_code != 200:
            logger.error(f"Instagram account receiving failed. {response.content=}")
            raise AuthenticationFailed()

        id = response.json().get('data')[0].get('instagram_business_account').get('id')
        return id

    def get_or_create_with_ig_token(self, ig_token: str):
        ig_id = self.get_user_ig_id(ig_token)
        ig_account, created = super().get_or_create(id = ig_id)
        ig_account.ig_token = ig_token
        ig_account.save()
        return ig_account, created


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"User {self.id}, {self.email}"


class InstagramAccount(models.Model):
    id = models.CharField(primary_key=True)
    access_token = models.CharField()
    last_login = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="ig_accounts")

    objects = InstagramAccountManager()

    def __str__(self):
        return f"IG account {self.id}, last accessed {self.last_login}"

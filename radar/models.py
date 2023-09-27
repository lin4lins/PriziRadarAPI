from urllib.parse import urlparse

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from radar.utils import get_account_ig_id, get_post_ig_id


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"User {self.id}, {self.email}"


class InstagramAccount(models.Model):
    ig_id = models.CharField(unique=True)
    access_token = models.CharField(unique=True)
    last_login = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="ig_accounts")

    def __str__(self):
        return f"IG account {self.id}, last accessed {self.last_login}"

    def save(self, *args, **kwargs):
        if not self.ig_id:
            self.ig_id = get_account_ig_id(self.access_token)

        super().save(*args, **kwargs)


class InstagramPost(models.Model):
    ig_id = models.CharField(unique=True)
    url = models.CharField()
    shortcode = models.CharField(unique=True)
    ig_account = models.ForeignKey(InstagramAccount,
                                   on_delete=models.CASCADE,
                                   related_name="ig_posts")

    def save(self, *args, **kwargs):
        if not self.shortcode:
            parsed_url = urlparse(self.url)
            path = parsed_url.path
            self.shortcode = path.strip('/').split('/')[-1]

        if not self.ig_id:
            self.ig_id = get_post_ig_id(self.ig_account.ig_id, self.shortcode,
                                        self.ig_account.access_token)

        super().save(*args, **kwargs)


class InstagramComment(models.Model):
    ig_post = models.ForeignKey(InstagramPost,
                                on_delete=models.CASCADE,
                                related_name="ig_comments")
    text = models.CharField(max_length=255)
    author_username = models.CharField(max_length=255)

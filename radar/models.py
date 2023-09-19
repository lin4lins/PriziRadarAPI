from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"User {self.id}, {self.email}"


class InstagramAccount(models.Model):
    id = models.CharField(primary_key=True)
    access_token = models.CharField(unique = True)
    last_login = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="ig_accounts")

    def __str__(self):
        return f"IG account {self.id}, last accessed {self.last_login}"

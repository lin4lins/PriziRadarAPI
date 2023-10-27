from django.db import models
from radar.utils import get_account_details, get_account_id


class AccountManager(models.Manager):
    def get_or_create(self, ig_token):
        account_id = get_account_id(ig_token)
        try:
            return self.get(id=account_id), False

        except Account.DoesNotExist:
            account_details = get_account_details(account_id, ig_token)
            return self.create(**account_details), True


class Account(models.Model):
    id = models.CharField(primary_key=True, unique=True)
    name = models.CharField()
    username = models.CharField(unique = True)
    profile_picture_url = models.CharField()

    objects = AccountManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "id"

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __str__(self):
        return f"IG account {self.id}, {self.username}"


class Connection(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='connections')
    ig_token = models.CharField(unique = True)

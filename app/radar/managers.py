from django.db import models
from radar.models import Account
from radar.utils.account import get_account_details, get_account_id


class AccountManager(models.Manager):
    def get_or_create(self, ig_token):
        account_id = get_account_id(ig_token)
        account_details = get_account_details(account_id, ig_token)
        return self.update_or_create(**account_details)

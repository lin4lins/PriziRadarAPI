from django.db import models

from radar.models import Account
from radar.utils import get_account_id, get_account_details


class AccountManager(models.Manager):
    def get_or_create(self, ig_token):
        account_id = get_account_id(ig_token)
        try:
            return self.get(id=account_id), False

        except Account.DoesNotExist:
            account_details = get_account_details(account_id, ig_token)
            return self.create(**account_details), True

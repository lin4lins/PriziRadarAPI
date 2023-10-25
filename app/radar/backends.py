from django.contrib.auth.backends import ModelBackend

from radar.models import Connection


class ConnectionBackend(ModelBackend):
    def authenticate(self, request, ig_token=None, **kwargs):
        try:
            connection = Connection.objects.get(ig_token = ig_token)
            return connection
        except Connection.DoesNotExist:
            return

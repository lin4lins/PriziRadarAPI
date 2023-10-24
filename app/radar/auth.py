from rest_framework.exceptions import AuthenticationFailed

from radar.models import Connection


def authenticate(connection_id: int):
    try:
        print('rnunfasdvxcfsdgbfcvawdsfcvwfesdgb')
        Connection.objects.get(id =connection_id)

    except Connection.DoesNotExist:
        raise AuthenticationFailed()

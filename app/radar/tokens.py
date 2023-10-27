from radar.models import Connection
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, Token


class ConnectionAccessToken(AccessToken):
    @classmethod
    def for_connection(cls, connection: Connection) -> Token:
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        connection_id = getattr(connection, api_settings.USER_ID_FIELD)
        if not isinstance(connection_id, int):
            connection_id = str(connection_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = connection_id

        return token

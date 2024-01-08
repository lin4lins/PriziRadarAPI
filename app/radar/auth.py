from typing import Optional, Tuple

from radar.models import Connection
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token


class ConnectionJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.connection_model = Connection()

    def authenticate(self, request: Request) -> Optional[Tuple[Connection, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        request.connection = self.get_connection(validated_token)
        request.account = request.connection.account
        return request.connection, validated_token

    def get_connection(self, validated_token: Token) -> Connection:
        try:
            connection_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise AuthenticationFailed()

        try:
            connection = Connection.objects.get(id=connection_id)
        except self.connection_model.DoesNotExist:
            raise AuthenticationFailed()

        return connection

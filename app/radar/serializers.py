from radar.models import Account, Connection
from radar.tokens import ConnectionAccessToken
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        read_only = ['name', 'username', 'avatar_url']


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'ig_token']
        write_only = ['ig_token']

    def create(self, validated_data):
        ig_token = validated_data.get('ig_token')
        account, is_created = Account.objects.get_or_create(ig_token = ig_token)
        connection = Connection(account = account, **validated_data)
        connection.save()
        return connection


class ConnectionTokenObtainSerializer(serializers.Serializer):
    token_class = ConnectionAccessToken
    ig_token = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        connection = self.create_connection(data)
        token = self.get_token(connection)
        return {'token': str(token), 'user': connection.account.to_dict()}

    @staticmethod
    def create_connection(attrs: dict) -> Connection:
        serializer = ConnectionSerializer(data = attrs)
        serializer.is_valid(raise_exception = True)
        return serializer.save()

    @classmethod
    def get_token(cls, connection):
        return cls.token_class.for_connection(connection)

from rest_framework import serializers

from radar.models import Account, Connection


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

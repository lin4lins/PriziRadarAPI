from rest_framework import serializers

from radar.models import User, InstagramAccount, InstagramPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class InstagramAccountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)

    class Meta:
        model = InstagramAccount
        fields = '__all__'
        read_only_fields = ["ig_id", "user"]


class InstagramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        exclude = ['ig_account']
        read_only_fields = ['ig_id', 'shortcode', 'ig_account']

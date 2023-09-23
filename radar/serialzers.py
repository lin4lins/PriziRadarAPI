from rest_framework import serializers

from radar.models import InstagramAccount, InstagramPost, User, InstagramComment


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
    id = serializers.CharField(read_only=True)

    class Meta:
        model = InstagramAccount
        fields = '__all__'
        read_only_fields = ["ig_id", "user"]


class InstagramPostSerializer(serializers.ModelSerializer):
    account_id = serializers.CharField(write_only=True)

    class Meta:
        model = InstagramPost
        exclude = ['ig_account']
        read_only_fields = ['ig_id', 'shortcode', 'ig_account']

    def create(self, validated_data):
        account_id = validated_data.pop('account_id')
        ig_account = InstagramAccount.objects.get(id = account_id)
        validated_data['ig_account'] = ig_account
        return super().create(validated_data)


class InstagramCommentSerializer(serializers.ModelSerializer):
    ig_post = serializers.PrimaryKeyRelatedField(queryset = InstagramPost.objects.all())

    class Meta:
        model = InstagramComment
        fields = '__all__'
        exclude = 'id'

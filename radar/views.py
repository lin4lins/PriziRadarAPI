import random

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from radar.models import InstagramAccount, User, InstagramComment
from radar.serialzers import (InstagramAccountSerializer,
                              InstagramCommentSerializer,
                              InstagramPostSerializer, UserSerializer)
from radar.utils import get_comments_by_post_instance


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]

        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return JsonResponse({
            "token": token.key,
            'user': serializer.data
        },
                            status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')


class InstagramAccountViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InstagramAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InstagramPostRandomCommentView(generics.GenericAPIView):
    serializer_class = InstagramPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ig_post = self.create_post(request.data)
        comments = get_comments_by_post_instance(
            ig_post, ig_post.ig_account.access_token)
        if comments:
            serialized_comments = self.serialize_comments(comments)
            random_comment = random.choice(serialized_comments)
            return JsonResponse({'comment': random_comment},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'No comments found'},
                                status=status.HTTP_404_NOT_FOUND)

    def create_post(self, request_data):
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return post

    @staticmethod
    def serialize_comments(comments):
        comment_instances = [
            InstagramComment(**comment_data) for comment_data in comments
        ]
        serialized_comments = InstagramCommentSerializer(comment_instances,
                                                         many=True)
        return serialized_comments.data


schema_view = get_schema_view(
    openapi.Info(
        title="PriziRadarAPI",
        default_version='v1',
        description="Descriptin",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="elina.vl.shramko@ygmail.com"),
        license=openapi.License(name="Elina Shramko"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

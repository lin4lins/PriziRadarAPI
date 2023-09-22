from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from radar.models import User, InstagramAccount, InstagramPost
from radar.serialzers import UserSerializer, InstagramAccountSerializer, InstagramPostSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]

        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user = serializer.instance)
        return JsonResponse({"token": token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)

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


class InstagramPostViewSet(viewsets.ModelViewSet):
    queryset = InstagramPost.objects.all()
    serializer_class = InstagramPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(ig_account__user=user)

    def perform_create(self, serializer):
        serializer.save(ig_account=self.request.user.ig_account)

from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from radar.serialzers import UserSerializer, InstagramAccountSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user = serializer.instance)
        return JsonResponse({"token": token.key})


class UserRetrieveView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class InstagramAccountCreateView(CreateAPIView):
    serializer_class = InstagramAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

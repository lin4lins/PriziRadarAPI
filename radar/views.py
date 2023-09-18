from django.http import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from radar.models import User
from radar.serialzers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        super().perform_create(serializer)
        token = Token.objects.create(user = serializer.instance)
        return JsonResponse({"token": token.key})

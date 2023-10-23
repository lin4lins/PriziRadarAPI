from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from radar.models import Connection
from radar.serializers import ConnectionSerializer


class ConnectionCreateView(generics.CreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user = serializer.instance.account)
        return JsonResponse({'token': token.key})

# class ConnectionDestroyView(generics.DestroyAPIView):
#     queryset = Connection.objects.filter()
#     serializer_class = ConnectionSerializer


schema_view = get_schema_view(
    openapi.Info(
        title="PriziRadarAPI",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="elina.vl.shramko@ygmail.com"),
        license=openapi.License(name="Elina Shramko"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

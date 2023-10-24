from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.authentication import JWTAuthentication

from radar.models import Connection
from radar.serializers import TokenObtainSerializer


class LogInView(TokenViewBase):
    queryset = Connection.objects.all()
    serializer_class = TokenObtainSerializer


class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return JsonResponse({"message": f"Welcome home! {request.user.account.username}"})


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

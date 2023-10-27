from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from radar import permissions
from radar.auth import ConnectionJWTAuthentication
from radar.models import Connection
from radar.serializers import ConnectionTokenObtainSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


class LogInView(TokenObtainPairView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionTokenObtainSerializer


class HomeView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return JsonResponse({"message": f"Welcome home! {request.connection.account.name}"})


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

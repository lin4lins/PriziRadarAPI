from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.exceptions import ValidationError

from radar import permissions
from radar.auth import ConnectionJWTAuthentication
from radar.models import Connection
from radar.serializers import ConnectionTokenObtainSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from radar.utils.comment import get_post_details


class LogInView(TokenObtainPairView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionTokenObtainSerializer


class PostGetView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        url_param = request.GET.get("url", None)
        if url_param is None:
            raise ValidationError("The 'url' parameter is required.")

        connection = request.connection
        post_details = get_post_details(connection.account.id, url_param, connection.ig_token)
        return JsonResponse(post_details)


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

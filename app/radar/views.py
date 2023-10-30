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

from radar.utils.post import IGPostFetcher


class LogInView(TokenObtainPairView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionTokenObtainSerializer


class PostView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        url = request.GET.get("url", None)
        if url is None:
            raise ValidationError("The 'url' parameter is required.")

        post_fetcher = IGPostFetcher(request.account.id, request.connection.ig_token, url)
        return JsonResponse(post_fetcher.post.to_dict())


class RandomCommentView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):

        comments_count = request.GET.get("url", 1)
        check_like = request.GET.get("check_likes", False)
        check_sub = request.GET.get("check_likes", False)


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

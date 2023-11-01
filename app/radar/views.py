from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from radar import permissions
from radar.auth import ConnectionJWTAuthentication
from radar.models import Connection
from radar.serializers import ConnectionTokenObtainSerializer
from radar.utils.comment import IGCommentFetcher
from radar.utils.post import IGPostFetcher
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


class LogInView(TokenObtainPairView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionTokenObtainSerializer
    permission_classes = [AllowAny]


class PostView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        url = request.GET.get("url", None)
        if url is None:
            raise ValidationError({'url': "Parameter is required."})

        post_fetcher = IGPostFetcher(request.account.id, request.connection.ig_token, url)
        try:
            post = post_fetcher.get_post()
        except (IndexError, TypeError):
            raise NotFound()

        return JsonResponse(post.to_dict())


class RandomCommentView(APIView):
    authentication_classes = [ConnectionJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        comments_count = request.GET.get("count", 1)

        comment_fetcher = IGCommentFetcher(id, request.connection.ig_token, request.account.id)
        try:
            comments = comment_fetcher.get_random_comments(comments_count)
        except ValueError:
            raise NotFound()

        return JsonResponse({"comments": [comment.to_dict() for comment in comments]})


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

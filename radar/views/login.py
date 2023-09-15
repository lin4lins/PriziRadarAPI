import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.exceptions import AuthenticationFailed

from logging_conf import logger
from radar.models import User
from radar.utils import get_facebook_oauth_url, get_facebook_token_url


# Create your views here.

class AuthorizationView(View):
    def get(self, request):
        if 'code' in request.GET:
            return self.authorize_user(request)
        else:
            return self.send_facebook_login_url()

    def authorize_user(self, request):
        authorization_code = request.GET.get('code')
        access_token = self.get_facebook_access_token(authorization_code)
        user, created = User.objects.get_or_create_with_ig_token(access_token)
        logger.error(f"Login completed. {user=}, {created=}")
        return HttpResponse(status = 201)

    @staticmethod
    def send_facebook_login_url():
        facebook_login_url = get_facebook_oauth_url()
        response_data = {'facebook_login_url': facebook_login_url}
        return JsonResponse(response_data)

    @staticmethod
    def get_facebook_access_token(authorization_code):
        facebook_token_url = get_facebook_token_url(authorization_code)
        response = requests.get(facebook_token_url)
        if response.status_code != 200:
            logger.error(f"Token receiving failed. {response.content=}")
            raise AuthenticationFailed()

        return response.json().get('access_token')

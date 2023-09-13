import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.exceptions import AuthenticationFailed

from logging_conf import logger
from radar.utils import get_facebook_oauth_url, get_facebook_token_url


# Create your views here.

class LogIn(View):
    def get(self, request):
        facebook_login_url = get_facebook_oauth_url()
        response_data = {'facebook_login_url': facebook_login_url}
        return JsonResponse(response_data)


class LogInCompleted(View):
    def get(self, request):
        authorization_code = request.GET.get('code', None)
        if not authorization_code:
            logger.error(f"Token receiving failed. Authorization code not found.")
            raise AuthenticationFailed()

        facebook_token_url = get_facebook_token_url(authorization_code)
        response = requests.get(facebook_token_url)
        if response.status_code != 200:
            logger.error(f"Token receiving failed. {response.content=}")
            raise AuthenticationFailed()

        logger.info("Token received successfully.")
        return HttpResponse(status=200)


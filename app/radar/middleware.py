from django.http import HttpResponseForbidden
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import AuthenticationFailed as SimpleAuthenticationFailed

from radar.auth import ConnectionJWTAuthentication


class ConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != '/login/':
            try:
                request.connection = ConnectionJWTAuthentication().authenticate(request)[0]
                request.account = request.connection.account

            except SimpleAuthenticationFailed as exp:
                return HttpResponseForbidden(exp.detail['detail'])

            except (AuthenticationFailed, TypeError) as exp:
                return HttpResponseForbidden(exp)

        response = self.get_response(request)
        return response

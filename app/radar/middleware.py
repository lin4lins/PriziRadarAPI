from radar.auth import ConnectionJWTAuthentication


class ConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.connection = ConnectionJWTAuthentication().authenticate(request)[0]
        response = self.get_response(request)
        return response

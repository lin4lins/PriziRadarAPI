import base64
import hashlib
import os

import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from dotenv import load_dotenv
from rest_framework.exceptions import AuthenticationFailed

from radar.utils import generate_code_verifier


# Create your views here.

class LogIn(View):
    @staticmethod
    def get_code_challenge(code_verifier: str) -> str:
        code_challenge_raw = base64.urlsafe_b64encode(code_verifier.encode())
        code_challenge_hash = hashlib.sha256(code_challenge_raw)
        return code_challenge_hash.hexdigest()

    def get_facebook_oauth_redirect_url(self) -> str:
        facebook_oauth_url = "https://www.facebook.com/v11.0/dialog/oauth"
        load_dotenv()
        code_verifier = generate_code_verifier()
        code_challenge = self.get_code_challenge(code_verifier)
        params = {
            "client_id": os.environ.get("CLIENT_ID"),
            "scope": "openid",
            "response_type": "code",
            "redirect_uri": f"http://localhost:8000/home/{code_verifier}",
            "state": "state123abc",
            "code_challenge": code_verifier,
            "code_challenge_method": "plain",
            "nonce": "123"
        }
        return f"{facebook_oauth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    def get(self, request):
        facebook_login_url = self.get_facebook_oauth_redirect_url()
        return redirect(facebook_login_url)


class Home(View):
    @staticmethod
    def get_facebook_exchange_endpoint(code_verifier, auth_code):
        facebook_token_url = "https://graph.facebook.com/v11.0/oauth/access_token"
        params = {
            "client_id": os.environ.get("CLIENT_ID"),
            "redirect_uri": f"http://localhost:8000/home/{code_verifier}",
            "code_verifier": code_verifier,
            "code": auth_code
        }
        return f"{facebook_token_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    def get(self, request, code_verifier):
        authorization_code = request.GET.get('code')
        facebook_token_url = self.get_facebook_exchange_endpoint(code_verifier, authorization_code)
        # response = requests.get(facebook_token_url)
        # if response.status_code != 200:
        #     raise AuthenticationFailed()

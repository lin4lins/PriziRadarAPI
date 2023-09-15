import os

from django.urls import reverse
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
MAIN_URL = "http://localhost:8000"


def get_facebook_oauth_url() -> str:
    facebook_oauth_url = "https://www.facebook.com/v17.0/dialog/oauth"
    params = {
        "client_id": CLIENT_ID,
        "scope": "openid",
        "response_type": "code",
        "redirect_uri": f"{MAIN_URL}{reverse('auth')}",
    }
    return f"{facebook_oauth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"


def get_facebook_token_url(authorization_code: str) -> str:
    facebook_token_url = "https://graph.facebook.com/v17.0/oauth/access_token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret":  CLIENT_SECRET,
        "redirect_uri": f"{MAIN_URL}{reverse('auth')}",
        "code": authorization_code
    }
    return f"{facebook_token_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"


def get_facebook_accounts_url(user_ig_token: str) -> str:
    facebook_accounts_url = "https://graph.facebook.com/v17.0/me/accounts"
    params = {
        "fields": "instagram_business_account",
        "access_token": user_ig_token,
    }
    return f"{facebook_accounts_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"


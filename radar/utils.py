import json
import os

import requests
from dotenv import load_dotenv
from rest_framework.exceptions import NotFound

load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
MAIN_URL = "http://localhost:8000"


def get_ig_business_accounts_url(user_ig_token: str) -> str:
    facebook_accounts_url = "https://graph.facebook.com/v17.0/me/accounts"
    params = {
        "fields": "instagram_business_account",
        "access_token": user_ig_token,
    }
    return f"{facebook_accounts_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"


def get_ig_account_id(access_token: str) -> str:
    response = requests.get(get_ig_business_accounts_url(access_token))
    if response.status_code != 200:
        raise NotFound()

    data_dict = json.loads(response.content)
    return data_dict["data"][0]["instagram_business_account"]["id"]

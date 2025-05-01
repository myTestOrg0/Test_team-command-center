import requests
import time
import jwt
from constants import *
import os

# note https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app

def get_access_token() -> str:
    """Return access token for GitHub API"""
    signing_key = token = os.environ.get('GH_APP_TOKEN')
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + 600,
        'iss': client_id
    }
    jwt_token = jwt.encode(payload, signing_key, algorithm='RS256')

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    response = requests.post(url=url, headers=headers)
    if response.status_code == 201:
        if "token" in response.json():
            return response.json()["token"]
        else:
            raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")
    else:
        raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")

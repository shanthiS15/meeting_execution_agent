import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")


def get_access_token():

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {encoded}"
    }

    params = {
        "grant_type": "account_credentials",
        "account_id": ACCOUNT_ID
    }

    response = requests.post(
        "https://zoom.us/oauth/token",
        headers=headers,
        params=params
    )

    data = response.json()

    print("Zoom Response:")
    print(data)

    if "access_token" not in data:
        raise Exception(
            f"Zoom Authentication Failed: {data}"
        )

    return data["access_token"]


def get_meetings():

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        "https://api.zoom.us/v2/users/me/meetings",
        headers=headers
    )

    return response.json()

def get_latest_zoom_transcript():

    with open(
        "sample_zoom_transcript.txt",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()
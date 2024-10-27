from typing import Annotated

from authlib.integrations.starlette_client import OAuth  # type: ignore
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=Secret)
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
DEVELOPER_TOKEN = config("DEVELOPER_TOKEN")
TRACKING_URL_TEMPLATE = config("TRACKING_URL_TEMPLATE")

OAUTH = OAuth()

OAUTH.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_params={"access_type": "offline", "prompt": "consent"},
    client_kwargs={
        "scope": "email openid profile https://www.googleapis.com/auth/adwords"
    },
)


def get_credentials(login_customer_id: str = None, refresh_token: str = None):
    temp = {
        "developer_token": DEVELOPER_TOKEN,
        "client_id": CLIENT_ID,
        "use_proto_plus": True,
        "client_secret": CLIENT_SECRET,
    }
    if login_customer_id:
        temp["login_customer_id"] = login_customer_id
    if refresh_token:
        temp["refresh_token"] = refresh_token
    return temp

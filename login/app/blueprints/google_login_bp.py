from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")


google_login_bp = OAuth2ConsumerBlueprint(
    "oauth-google", __name__,
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url="http://dev1.dmtool.info",
    token_url="http://dev1.dmtool.info/app/login/google/access_token",
    authorization_url="http://dev1.dmtool.info/app/login/google/authorize",
)

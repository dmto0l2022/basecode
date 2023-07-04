from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint

google_login_bp = OAuth2ConsumerBlueprint(
    "oauth-google", __name__,
    client_id="my-key-here",
    client_secret="my-secret-here",
    base_url="http://dev1.dmtool.info",
    token_url="http://dev1.dmtool.info/app/login/google/access_token",
    authorization_url="http://dev1.dmtool.info/app/login/google/authorize",
)

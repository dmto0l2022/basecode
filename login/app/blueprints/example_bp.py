from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import Flask, redirect, url_for

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

example_blueprint = OAuth2ConsumerBlueprint("google", __name__,
                                    client_id=GOOGLE_CLIENT_ID,
                                    client_secret=GOOGLE_CLIENT_SECRET,
                                    scope=None,
                                    base_url="http://dev1.dmtool.info/",
                                    authorization_url="http://dev1.dmtool.info/login/oauth/authorize",
                                    token_url="https://github.com/login/oauth/access_token",
                                    redirect_url=None,
                                    redirect_to=None,
                                    login_url=None,
                                    authorized_url=None,
                                    session_class=None,
                                    backend=None,
                                    )


@example_blueprint.route('/login')
def login():
    if not example_blueprint.authorized:
        return redirect(url_for('example_blueprint.login'))
    try:
        account_info=example_blueprint.session.get("/user")
        print "i m here ....."
        print account_info.ok
        return account_info
    except Exception as e:
        print "i m here .....",e

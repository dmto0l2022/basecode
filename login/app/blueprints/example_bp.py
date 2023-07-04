from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import Flask, redirect, url_for


client_id = "*********************",
client_secret = "********************",

example_blueprint = OAuth2ConsumerBlueprint("github", __name__,
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    scope=None,
                                    base_url="https://api.github.com/",
                                    authorization_url="https://github.com/login/oauth/authorize",
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

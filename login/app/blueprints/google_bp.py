from flask_dance.contrib.google import make_google_blueprint, google

google_blueprint = make_google_blueprint(
    client_id='YOUR-CLIENT-ID-HERE',
    client_secret='YOUR-CLIENT-SECRET-HERE',
    scope=['https://www.googleapis.com/auth/userinfo.email',
           'https://www.googleapis.com/auth/userinfo.profile'],
    offline=True,
    reprompt_consent=True,
    backend=SQLAlchemyBackend(OAuth, db.session, user=current_user)
)

app.register_blueprint(google_blueprint)

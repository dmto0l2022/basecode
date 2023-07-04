from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

blueprint = make_google_blueprint(
    client_id="my-key-here",
    client_secret="my-secret-here",
    scope=["profile", "email"]
)

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])

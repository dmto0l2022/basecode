## https://testdriven.io/blog/flask-sessions/
from flask import Blueprint, render_template, Flask, render_template_string, request, redirect, url_for, g
from flask_restful import Api, Resource, url_for
import datetime

from flask import session

from flask_security import current_user

from flask.json import jsonify
import requests
from requests_oauthlib import OAuth2Session

from os import environ, path
from dotenv import load_dotenv

import requests
import json

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

session_bp = Blueprint('session_bp', __name__)

def createsessionid():
    sessionidnow = datetime.datetime.utcnow().strftime("S%Y%m%d%H%M%S%f")
    return sessionidnow


@session_bp.route('/app/session', methods=['GET', 'POST'])
def sessionroot():
    return 'session root'


@session_bp.route('/app/session/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        session['sessionid'] = createsessionid()
        return redirect(url_for('session_bp.get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@session_bp.route('/app/session/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('session_bp.set_email') }}">here.</a></h1>
            {% endif %}
            <h1>Session ID : {{ session['sessionid'] }}</h1>
            
            {% for key, value in session.items() %}
              <h1>Key: {{key}}</h1>
              <h2>Value: {{value}}</h2>
           {% endfor %}
        """)
'''
@session_bp.route('/app/session/showsession')
def showsession():
    return render_template_string("""{% for key, value in session.items() %} Key: {{key}} Value: {{value}} {% endfor %}""")
'''
@session_bp.route('/app/session/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    session.pop('sessionid', default=None)
    return '<h1>Session deleted!</h1>'


@session_bp.route('/app/session/setsession')
def setsession():
    try:
        #session['UserID'] = current_user.get_id()
        #session['Username'] = current_user.username()
        #session['SessionID'] =  createsessionid()
        if current_user.is_authenticated:
            #g.user = current_user.get_id()
            session['Username'] = current_user.username
        return f"The session has been Set"
    except:
        return f"The session has NOT been Set"
 
@session_bp.route('/app/session/getsession')
def getsession():
    #if 'Username' in session:
    # Username = session['Username']
    try:
        dmtool_userid = session['dmtool_userid']
        #UserID =  session['UserID']
        #SessionID = session['SessionID']
        return f"Welcome DMTool User {dmtool_userid} " ## your userid is {UserID} and sessionid {SessionID}"
    except:
        return "Welcome Anonymous"

@session_bp.route('/app/session/googlesession')
def getgooglesession():
    try:
        print("session_bp - oauth_token >>>> ",session['oauth_token'])
        google = OAuth2Session(GOOGLE_CLIENT_ID, token=session['oauth_token'])
        profile_json = jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
        data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        google_id = data['id']
        print('google_id >>>>',google_id)
        return f"Welcome google id >> {google_id} " ## your userid is {UserID} and sessionid {SessionID}"
    except:
        return f"No Google Session"

@session_bp.route('/app/session/getgoogleid')
def getgoogleid():
    try:
        google = OAuth2Session(GOOGLE_CLIENT_ID, token=session['oauth_token'])
        profile_json = jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
        data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        google_id = data['id']
        print('google_id >>>>',google_id)
        return jsonify({'google_id':google_id})
    except:
        return jsonify({'google_id':'99999999'})

@session_bp.route('/app/session/popsession')
def popsession():
    for key in list(session.keys()):
         session.pop(key)
    return "Session Deleted"

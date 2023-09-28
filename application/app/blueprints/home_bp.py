from flask import Blueprint, render_template

from flask_security import Security, SQLAlchemyUserDatastore, auth_required

from flask_security.models import fsqla_v3 as fsqla

from flask_login import current_user

import random

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/app/', methods=['GET', 'POST'])
def rootofserver():
    return 'the name is root'

@home_bp.route('/app/home')
def home():
    return render_template('home.html')

# Views
@home_bp.route("/app/heart")
def heart():
    return render_template_string('Home is where the heart is !')

@home_bp.route("/app/hello")
@auth_required()
def hello():
    return render_template_string('Hello {{email}} !', email=current_user.email)

@home_bp.route('/app/welcome/')
@auth_required()
def welcome():
    return render_template('welcome.html')


@home_bp.route('/app/dash/')
def homepage():
    return """
    <h1>Hello world!</h1>

    <iframe src="../wsgi_app2" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    """



'''
@home_bp.route('/app/dash/')
def dashit():
    urls = [
        'http://www.w3schools.com',
        'http://techcrunch.com/',
        'https://www.fayerwayer.com/',
    ]

    iframe = random.choice(urls)

    return render_template('iframe.html', iframe=iframe)
'''

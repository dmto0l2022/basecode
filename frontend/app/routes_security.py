#from flask import render_template
from flask import render_template, flash, redirect, url_for

from flask import Flask, render_template_string

##from app import app
from flask import current_app

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password

from flask_login import current_user

from flask_security.models import fsqla_v3 as fsqla

# Views
@current_app.route("/")
def home():
    return render_template_string('Home is where the heart is !')

@current_app.route("/hello")
@auth_required()
def hello():
    return render_template_string('Hello {{email}} !', email=current_user.email)

@current_app.route('/app/welcome/')
@auth_required()
def welcome():
    return render_template('welcome.html')

from flask import Blueprint, render_template, session, render_template_string
from app.models import UserSimple
from app.models import User

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/app/users/getall')
def getallusers():
    users = UserSimple.get_users()
    return render_template('users_simple.html', users=users)

@users_bp.route('/app/users/setsession')
def setsession():
    userid = session['_user_id']
    all_ret = User.get_user(userid)
    email_ret = all_ret.email
    session['useremail'] = all_ret.email
    return render_template_string('hello {{ what }}', what=email_ret)

@users_bp.route('/app/users/getusername')
def getusername():
    userid = session['_user_id']
    username_full = User.get_username(userid)
    return render_template_string('hello {{ what }}', what=userid)

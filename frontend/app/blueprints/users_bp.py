from flask import Blueprint, render_template, session
from app.models import UserSimple
from app.models import User

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/app/users/getall')
def getallusers():
    users = UserSimple.get_users()
    return render_template('users_simple.html', users=users)

@users_bp.route('/app/users/getusername')
def getusername():
    userid = session['_user_id']
    username_full = User.get_username()
    return render_template_string('hello {{ what }}', what=username_full)

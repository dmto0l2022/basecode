from flask import Blueprint, render_template, session
from app.models import UserSimple
from app.models import UserSimple
users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/app/users/getall')
def index():
    users = UserSimple.get_users()
    return render_template('users_simple.html', users=users)

@users_bp.route('/app/users/getusername')
def index():
    userid = session['_user_id']
    username_full = User.get_username()
    return render_template_string('hello {{ what }}', what=username_full)

from flask import Blueprint, render_template
from app.models import UserSimple

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/app/users/getall')
def index():
    users = UserSimple.get_users()
    return render_template('users_simple.html', users=users)

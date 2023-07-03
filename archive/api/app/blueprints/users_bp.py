from flask import Blueprint, render_template
from app.models import User

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/')
def index():
    users = User.get_users()
    return render_template('users_simple.html', users=users)

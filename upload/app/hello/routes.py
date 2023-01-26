from flask import Blueprint
hello_page_bp = Blueprint('hello_page_bp', __name__)

@hello_page_bp.route('/')
def index():
     return "Hello"

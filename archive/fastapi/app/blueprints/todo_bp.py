from flask import Blueprint, render_template

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/todo', methods=['GET', 'POST'])
def todoroot():
    return 'todo root'

@todo_bp.route('/todo/home')
def todohome():
    return 'todo home'


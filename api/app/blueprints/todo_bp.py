from flask import Blueprint, render_template
from flask_restful import Api, Resource, url_for

todo_bp = Blueprint('todo_bp', __name__)
api = Api(todo_bp)

@todo_bp.route('/todo', methods=['GET', 'POST'])
def todoroot():
    return 'todo root'

@todo_bp.route('/todo/home')
def todohome():
    return 'todo home'

class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todo/list/<int:id>')

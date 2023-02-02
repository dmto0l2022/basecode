from flask import Flask
from flask import flash

import os
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

def init_app():
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
   
    from app.blueprints.todo_bp import todo_bp
    app.register_blueprint(todo_bp)
    
    return app


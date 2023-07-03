"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Database setup
#db = SQLAlchemy()

from app.database import AppDb

app_db = AppDb()

def init_app():
    """Create Flask application."""
    flask_app = Flask(__name__, instance_relative_config=False)
    app_db.init_app(flask_app)
    
    #db.init_app(flask_app)  # initialise the database for the app

    with flask_app.app_context():
        from app.models import User  # this import allows us to create the table if it does not exist
        from app import create_users as cu
        dbModel.metadata.create_all(bind=app_db.engine)
        dbModel.query = app_db.session.query_property()

        from app.blueprints.users_bp import users_bp
        flask_app.register_blueprint(users_bp)
        return flask_app

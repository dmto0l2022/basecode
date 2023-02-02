from flask import Flask

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        
        # Register Blueprints
        app.register_blueprint(blueprints.todo_bp)

        return app


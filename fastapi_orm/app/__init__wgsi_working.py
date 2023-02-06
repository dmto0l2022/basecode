from flask import Flask

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        
        # Register Blueprints
        from app.blueprints.todo_bp import todo_bp
        app.register_blueprint(todo_bp)
        
        return app


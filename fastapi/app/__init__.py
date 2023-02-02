from flask import Flask

from typing import Union

from fastapi import FastAPI

def init_app():
    """Initialize the core application."""
    
    app = FastAPI()

    with app.app_context():
        
        @app.get("/")
        def read_root():
            return {"Hello": "World"}


        @app.get("/items/{item_id}")
        def read_item(item_id: int, q: Union[str, None] = None):
            return {"item_id": item_id, "q": q}

        
        return app

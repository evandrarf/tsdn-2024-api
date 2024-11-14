from flask import Flask, jsonify
from .config import Config
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description
            }
        }).data
        response.content_type = "application/json"
        return response
    
    with app.app_context():
        from .routes import init_app
    
    init_app(app)
    
    return app
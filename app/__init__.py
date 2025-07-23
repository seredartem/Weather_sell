from flask import Flask
from .config import Config
from .db import init_pool

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_pool(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
from flask import Flask
from app.routes import inventory_bp
from app.database import init_database


def create_app():
    app = Flask(__name__)
    app.register_blueprint(inventory_bp)
    init_database()
    return app

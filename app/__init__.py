from flask import Flask
from app.routes import inventory_bp
from app.database import init_database
import os


def create_app():
    # Get the path to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize Flask app with custom static folder
    app = Flask(__name__, 
                template_folder=os.path.join(app_dir, 'templates'),
                static_folder=os.path.join(app_dir, 'static'),
                static_url_path='/static')
    
    app.register_blueprint(inventory_bp)
    init_database()
    return app

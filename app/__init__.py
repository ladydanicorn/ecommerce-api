from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Apply CORS to ALL routes
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    
    app.config.from_object(Config)
    db.init_app(app)
    
    from .routes import customer_routes, product_routes, order_routes
    app.register_blueprint(customer_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(order_routes.bp)
    
    return app

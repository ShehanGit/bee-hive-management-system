# # app/__init__.py
# from flask import Flask
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import os

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)

#     CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    
#     # Load default configuration (from app/config.py)
#     app.config.from_object('app.config.Config')
    
#     # Load instance configuration (from instance/config.py) if it exists
#     # This can override any default settings (e.g., environment-specific credentials)
#     app.config.from_pyfile('config.py', silent=True)
    
#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
    
#     # Register Blueprints (routes)
#     from app.routes.api import api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')

#     # Start the APScheduler job for periodic sensor data fetching
#     if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#         from app.scheduler import start_scheduler
#         start_scheduler(app)
    
#     return app


# app/__init__.py
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
import os

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    # Load default configuration (from app/config.py)
    app.config.from_object('app.config.Config')
    
    # Load instance configuration (from instance/config.py) if it exists
    # This can override any default settings (e.g., environment-specific credentials)
    app.config.from_pyfile('config.py', silent=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register Blueprints (routes)
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Start the APScheduler job for periodic sensor data fetching
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        from app.scheduler import start_scheduler
        start_scheduler(app, socketio)
    
    return app


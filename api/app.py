"""Main quakelabs sms application and routing logic"""
from flask import Flask, json, jsonify, request
from api.routes.main_routes import main_routes
from flask_cors import CORS

# Logging
import logging


def create_app():
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    # Registering routes
    app.register_blueprint(main_routes)

    # Logging
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Application logging set")
    app.logger.info("SMS App started")
    return app

"""Main quakelabs sms application and routing logic"""
from flask import Flask, json, jsonify, request
from api.routes.main_routes import main_routes


def create_app():
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)

    # Registering routes
    app.register_blueprint(main_routes)

    return app

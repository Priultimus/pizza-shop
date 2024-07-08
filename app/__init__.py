import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()
logging.basicConfig(level=Config.LOG_LEVEL)


def init_app():
    """Initialize the API."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from .resources import CreateFood, CreateAddon, ManageFood, ManageAddon
        from .api import ExtendedAPI

        db.create_all()
        api = ExtendedAPI(app)
        api.add_resource(CreateFood, "/api/menu/food")
        api.add_resource(ManageFood, "/api/menu/food/<int:entity_id>")
        api.add_resource(CreateAddon, "/api/menu/addon")
        api.add_resource(ManageAddon, "/api/menu/addon/<int:entity_id>")
        return app

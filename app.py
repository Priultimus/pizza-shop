from flask import request, jsonify
from flask import Flask
from flask_restful import Api
from core import Controller
from errors import GENERIC_SERVER_ERROR
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES
from resources import ManageFood, CreateFood
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)


class ExtendedAPI(Api):
    """This class overrides 'handle_error' method of 'Api' class ,
    to extend global exception handing functionality of 'flask-restful'.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_error(self, err):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        print(err)  # log every exception raised in the application
        # Handle HTTPExceptions
        if isinstance(err, HTTPException):
            return {
                "success": False,
                "message": getattr(
                    err, "description", HTTP_STATUS_CODES.get(err.code, "")
                ),
            }, err.code
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, "message", None):
            return {
                "success": False,
                "message": "An unexpected error occurred",
                "code": GENERIC_SERVER_ERROR,
            }, 500
        # Handle application specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code


api = ExtendedAPI(app)


def log_exception(sender, exception, **extra):

    logger.error(f"An exception occurred: {exception}!!!!")
    logger.error(f"Extra: {extra}")


core = Controller(
    db_url="mysql+mysqlconnector://flask:password@127.0.0.1:3306/pizza_shop"
)

api.add_resource(
    ManageFood, "/api/menu/food/<int:entity_id>", resource_class_kwargs={"core": core}
)
api.add_resource(CreateFood, "/api/menu/food", resource_class_kwargs={"core": core})

if __name__ == "__main__":
    core.bootstrap()
    app.run(debug=True)

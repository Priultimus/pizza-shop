import logging

from flask import jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from .errors import GENERIC_SERVER_ERROR, ENTRY_NOT_FOUND, MISSING_ENTRY_DATA


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
        logger = logging.getLogger("handle_error")
        if not getattr(err, "code", None) in [
            ENTRY_NOT_FOUND,
            MISSING_ENTRY_DATA,
        ]:  # common errors
            logger.exception(err)
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

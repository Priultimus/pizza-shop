import logging

from flask import jsonify
from flask_restful import Api  # type: ignore
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
        """Handle all errors through the program, logs them and returns JSON error"""
        logger = logging.getLogger("handle_error")
        # Handle HTTPExceptions
        if isinstance(err, HTTPException):
            return {
                "success": False,
                "message": getattr(
                    err, "description", HTTP_STATUS_CODES.get(err.code, "")
                ),
                "data": {},
                "code": GENERIC_SERVER_ERROR,
            }, err.code

        # If message & code attributes are not set, consider it as Python core exception and hide sensitive error info from end user
        # Otherwise, handle application specific custom exceptions
        
        # Don't pass SQLALCHEMY error codes to the client
        code = getattr(err, "code", GENERIC_SERVER_ERROR)
        try:
            code = int(code)
        except ValueError:
            logger.warning(f"Exception thrown had code {code} - replacing with GENERIC_SERVER_ERROR")
            code = GENERIC_SERVER_ERROR

        response = {
            "success": getattr(err, "success", False),
            "message": getattr(err, "message", "An unexpected error occurred"),
            "data": getattr(err, "data", {}),  # additional data (if any)
            "code": code,
        }, getattr(err, "http_status_code", 500)
        if not response[0]["code"] in [
            ENTRY_NOT_FOUND,
            MISSING_ENTRY_DATA,
        ]:  # common errors
            logger.exception(err)

        return response

import logging

from flask import jsonify
from flask_restful import Api  # type: ignore
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from .errors import (
    GeneralException,
    GENERIC_SERVER_ERROR,
    ENTRY_NOT_FOUND,
    MISSING_ENTRY_DATA,
    GENERIC_BAD_REQUEST,
)


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
        is_http_exception = False
        if isinstance(
            err, HTTPException
        ):  # XXX: Surely there's a better way to do this
            is_http_exception = True
            err.message = HTTP_STATUS_CODES.get(err.code)
            if err.code == 400:
                err.http_status_code = err.code
                err.code = GENERIC_BAD_REQUEST
            else:
                err.code = GENERIC_SERVER_ERROR

        elif isinstance(err, GeneralException):
            err.code = getattr(err, "code", GENERIC_SERVER_ERROR)

        # If message & code attributes are not set, consider it as Python core exception and hide sensitive error info from end user
        # Otherwise, handle application specific custom exceptions
        else:
            # Don't pass non-documented error codes to the client
            if getattr(err, "code", None):
                logger.warning(
                    f"Exception thrown had code {err.code} - replacing with GENERIC_SERVER_ERROR"
                )
            err.code = GENERIC_SERVER_ERROR
            if getattr(err, "message", None):
                err.message = "An unexpected error occurred"
            err.code = getattr(err, "code", GENERIC_SERVER_ERROR)

        response = {
            "success": getattr(err, "success", False),
            "message": getattr(err, "message", "An unexpected error occurred"),
            "data": getattr(err, "data", {}),  # additional data (if any)
            "code": getattr(err, "code", GENERIC_SERVER_ERROR),
        }, getattr(err, "http_status_code", 500)

        if (
            not response[0]["code"] in self.app.config["SILENT_EXCEPTIONS"]
            or is_http_exception  # XXX: Remove or change whenever handling HTTPExceptions is concrete
        ):  # common errors
            logger.exception(err)

        return response

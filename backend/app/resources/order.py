import logging

from flask_restful import Resource  # type: ignore
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    MissingEntryData,
)


class CreateOrder(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateOrder")

    def get(self):
        print("hello")
        return {"success": True, "message": "", "code": 0, "data": {}}


class ManageOrder(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageOrder")

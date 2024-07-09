import logging

from flask_restful import Resource
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


class ManageOrder(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageOrder")

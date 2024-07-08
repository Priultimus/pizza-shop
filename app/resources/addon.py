import logging

from flask_restful import Resource
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    MissingEntryData,
)


class CreateAddon(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateAddon")

    def post(self):
        data = request.get_json()
        addon_data = data.get("addon")
        if not addon_data or not {"name", "type", "price"} <= set(addon_data):
            raise MissingEntryData
        addon = core.create.addon(
            addon_data.get("name"),
            addon_data.get("type"),
            addon_data.get("price"),
            addon_size=addon_data.get("size"),
        )
        return {"success": True, "message": "", "code": 0, "data": addon}


class ManageAddon(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageAddon")

    def get(self, entity_id):
        entity = core.find.addon(entity_id)
        if entity:
            return {"success": True, "message": "", "code": 0, "data": entity}
        else:
            raise EntryNotFound

    def delete(self, entity_id):
        addon = core.delete.addon(entity_id)
        if not addon:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}

    def put(self, entity_id):
        data = request.get_json()
        if not data.get("addon"):
            raise MissingEntryData
        addon_data = data.get("addon")

        addon_entity = core.find.addon(entity_id)
        if not addon_entity:
            raise EntryNotFound

        addon_data = data.get("addon")

        if not addon_data:
            raise MissingEntryData

        failure = []
        total_values = 0
        success = True

        if addon_data.get("name"):
            total_values += 1
            result = core.update.addon_name(entity_id, addon_data.get("name"))
            if not result:
                success = False
                failure.append("name")

        if addon_data.get("type"):
            total_values += 1
            result = core.update.addon_type(entity_id, addon_data.get("type"))
            if not result:
                success = False
                failure.append("type")

        if addon_data.get("price"):
            total_values += 1
            result = core.update.addon_price(entity_id, addon_data.get("price"))
            if not result:
                success = False
                failure.append("price")

        if addon_data.get("size"):
            total_values += 1
            result = core.update.addon_size(entity_id, addon_data.get("size"))
            if not result:
                success = False
                failure.append("size")

        if success:
            return {"success": True, "message": "", "code": 0, "data": {}}

        if len(failure) == total_values:
            raise EntryNotFound

        raise DataInconsistencyError

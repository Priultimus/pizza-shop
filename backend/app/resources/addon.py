import logging

from flask_restful import Resource  # type: ignore
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    MissingEntryData,
    ImproperEntryData,
    PARTIAL_SUCCESS
)


class CreateAddon(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateAddon")

    def post(self):
        data = request.get_json()
        addon_data = data.get("addon")
        if not addon_data or not {"name", "type", "price"} <= set(addon_data):
            raise MissingEntryData
        addon = core.creator.addon(
            addon_data.get("name"),
            addon_data.get("type"),
            addon_data.get("price"),
            addon_size=addon_data.get("size"),
        )
        return {"success": True, "message": "", "code": 0, "data": addon}


class ManageAddon(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageAddon")

    def get(self, addon_id):
        entity = core.finder.addon(addon_id)
        if entity:
            return {"success": True, "message": "", "code": 0, "data": entity}
        else:
            raise EntryNotFound

    def delete(self, addon_id):
        addon = core.deletor.addon(addon_id)
        if not addon:
            raise EntryNotFound
        return {
            "success": True, 
            "message": "", 
            "code": 0, 
            "data": {}
            }, 204

    def put(self, addon_id):
        data = request.get_json()
        if not data.get("addon"):
            raise MissingEntryData
        addon_data = data.get("addon")

        addon_entity = core.finder.addon(addon_id)
        if not addon_entity:
            raise EntryNotFound

        addon_data = data.get("addon")

        if not addon_data:
            raise MissingEntryData

        attempted_entries = {}

        if addon_data.get("name"):
            attempted_entries["name"] = True
            result = core.updater.addon_name(addon_id, addon_data.get("name"))
            if not result:
                attempted_entries["name"] = False

        if addon_data.get("type"):
            attempted_entries["type"] = True
            result = core.updater.addon_type(addon_id, addon_data.get("type"))
            if not result:
                attempted_entries["type"] = False

        if addon_data.get("price"):
            attempted_entries["price"] = True
            result = core.updater.addon_price(addon_id, addon_data.get("price"))
            if not result:
                attempted_entries["price"] = False

        if addon_data.get("size"):
            attempted_entries["size"] = True
            result = core.updater.addon_size(addon_id, addon_data.get("size"))
            if not result:
                attempted_entries["size"] = False
        
        if not len(attempted_entries): 
            # no useful data was provided by the user
            raise ImproperEntryData

        data = core.finder.addon(addon_id)
        success = all(attempted_entries.values())

        if not data: 
            # between updating the data and fetching it again, it vanished!
            raise DataInconsistencyError

        if success: 
            return {
                "success": True, 
                "message": "", 
                "code": 0, 
                "data": data
            }

        return {
            "success": False, 
            "message": "Some items did not successfully update. ", 
            "code": PARTIAL_SUCCESS, 
            "data": data,
            "results": attempted_entries
        }, 207
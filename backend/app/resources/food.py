import logging

from flask_restful import Resource  # type: ignore
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    ImproperEntryData,
    DataInconsistencyError,
    MissingEntryData,
    PARTIAL_SUCCESS
)


class CreateFood(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateFood")

    def post(self):
        data = request.get_json()
        food_data = data.get("food")
        if not food_data or not {"name", "price", "category"} <= set(food_data):
            raise MissingEntryData
        food = core.create.food(
            food_data.get("name"),
            food_data.get("price"),
            food_data.get("category"),
            food_size=food_data.get("size"),
        )
        if food:
            return {"success": True, "message": "", "code": 0, "data": food}
        else:
            raise ImproperEntryData("Food size is required for this category.")


class ManageFood(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageFood")

    def get(self, entity_id):
        entity = core.find.food(entity_id)
        if entity:
            return {"success": True, "message": "", "code": 0, "data": entity}
        else:
            raise EntryNotFound

    def delete(self, entity_id):
        food = core.delete.food(entity_id)
        if not food:
            raise EntryNotFound
        return {
            "success": True, 
            "message": "", 
            "code": 0, 
            "data": {}
            }, 204

    def put(self, entity_id):
        data = request.get_json()
        food_data = data.get("food")
        if not food_data:
            raise MissingEntryData

        food_entity = core.find.food(entity_id)
        if not food_entity:
            raise EntryNotFound

        attempted_entries = {}

        if food_data.get("name"):
            attempted_entries["name"] = True
            if not core.update.food_name(entity_id, food_data.get("name")):
                attempted_entries["name"] = False

        if food_data.get("price"):
            attempted_entries["price"] = True
            if not core.update.food_price(entity_id, food_data.get("price")):
                attempted_entries["price"] = False

        if food_data.get("category"):
            attempted_entries["category"] = True
            if not core.update.food_category(entity_id, food_data.get("category")):
                attempted_entries["category"] = False

        if food_data.get("size"):
            attempted_entries["size"] = True
            if not core.update.food_size(entity_id, food_data.get("size")):
                attempted_entries["size"] = False

        if not len(attempted_entries): 
            # no useful data was provided by the user
            raise ImproperEntryData

        data = core.find.food(entity_id)
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

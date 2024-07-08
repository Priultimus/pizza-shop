from flask_restful import Resource
from flask import request
from errors import (
    EntryNotFound,
    MissingFoodSize,
    DataInconsistencyError,
    MissingEntryData,
)
from core import Controller
import logging


class CreateFood(Resource):
    def __init__(self, core: Controller):
        self.core = core
        self.logger = logging.getLogger("CreateFood")

    def post(self):
        data = request.get_json()
        food_data = data.get("food")
        if not food_data or not {"name", "price", "category"} <= set(food_data):
            raise MissingEntryData
        food = self.core.create_food(
            food_data.get("name"),
            food_data.get("price"),
            food_data.get("category"),
            food_size=food_data.get("size"),
        )
        if food:
            return {"success": True, "message": "", "code": 0, "data": food}
        else:
            raise MissingFoodSize


class CreateAddon(Resource):
    def __init__(self, core: Controller):
        self.core = core
        self.logger = logging.getLogger("CreateAddon")

    def post(self):
        data = request.get_json()
        addon_data = data.get("addon")
        if not addon_data or not {"name", "type", "price"} <= set(addon_data):
            raise MissingEntryData
        addon = self.core.create_addon(
            addon_data.get("name"),
            addon_data.get("type"),
            addon_data.get("price"),
            addon_size=addon_data.get("size"),
        )
        return {"success": True, "message": "", "code": 0, "data": addon}


class ManageFood(Resource):
    def __init__(self, core: Controller):
        self.core = core
        self.logger = logging.getLogger("ManageFood")

    def get(self, entity_id):
        entity = self.core.find_food(entity_id)
        if entity:
            return {"success": True, "message": "", "code": 0, "data": entity}
        else:
            raise EntryNotFound

    def delete(self, entity_id):
        food = self.core.delete_food(entity_id)
        if not food:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}

    def put(self, entity_id):
        data = request.get_json()
        if not data.get("food"):
            raise MissingEntryData
        food_data = data.get("food")

        food_entity = self.core.find_food(entity_id)
        if not food_entity:
            raise EntryNotFound

        food_data = data.get("food")

        if not food_data:
            raise MissingEntryData

        failure = []
        total_values = 0
        success = True

        if food_data.get("name"):
            total_values += 1
            result = self.core.update_food_name(entity_id, food_data.get("name"))
            if not result:
                success = False
                failure.append("name")

        if food_data.get("price"):
            total_values += 1
            result = self.core.update_food_price(entity_id, food_data.get("price"))
            if not result:
                success = False
                failure.append("price")

        if food_data.get("category"):
            total_values += 1
            result = self.core.update_food_category(
                entity_id, food_data.get("category")
            )
            if not result:
                success = False
                failure.append("category")

        if food_data.get("size"):
            total_values += 1
            result = self.core.update_food_size(entity_id, food_data.get("size"))
            if not result:
                success = False
                failure.append("size")

        if success:
            return {"success": True, "message": "", "code": 0, "data": {}}

        if len(failure) == total_values:
            raise EntryNotFound

        raise DataInconsistencyError


class ManageAddon(Resource):
    def __init__(self, core: Controller):
        self.core = core
        self.logger = logging.getLogger("ManageAddon")

    def get(self, entity_id):
        entity = self.core.find_addon(entity_id)
        if entity:
            return {"success": True, "message": "", "code": 0, "data": entity}
        else:
            raise EntryNotFound

    def delete(self, entity_id):
        addon = self.core.delete_addon(entity_id)
        if not addon:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}

    def put(self, entity_id):
        data = request.get_json()
        if not data.get("addon"):
            raise MissingEntryData
        addon_data = data.get("addon")

        addon_entity = self.core.find_addon(entity_id)
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
            result = self.core.update_addon_name(entity_id, addon_data.get("name"))
            if not result:
                success = False
                failure.append("name")

        if addon_data.get("type"):
            total_values += 1
            result = self.core.update_addon_type(entity_id, addon_data.get("type"))
            if not result:
                success = False
                failure.append("type")

        if addon_data.get("price"):
            total_values += 1
            result = self.core.update_addon_price(entity_id, addon_data.get("price"))
            if not result:
                success = False
                failure.append("price")

        if addon_data.get("size"):
            total_values += 1
            result = self.core.update_addon_size(entity_id, addon_data.get("size"))
            if not result:
                success = False
                failure.append("size")

        if success:
            return {"success": True, "message": "", "code": 0, "data": {}}

        if len(failure) == total_values:
            raise EntryNotFound

        raise DataInconsistencyError

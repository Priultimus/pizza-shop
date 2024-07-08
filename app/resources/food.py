import logging

from flask_restful import Resource
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    MissingFoodSize,
    DataInconsistencyError,
    MissingEntryData,
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
            raise MissingFoodSize


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
        return {"success": True, "message": "", "code": 0, "data": {}}

    def put(self, entity_id):
        data = request.get_json()
        if not data.get("food"):
            raise MissingEntryData
        food_data = data.get("food")

        food_entity = core.find.food(entity_id)
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
            result = core.update.food_name(entity_id, food_data.get("name"))
            if not result:
                success = False
                failure.append("name")

        if food_data.get("price"):
            total_values += 1
            result = core.update.food_price(entity_id, food_data.get("price"))
            if not result:
                success = False
                failure.append("price")

        if food_data.get("category"):
            total_values += 1
            result = core.update.food_category(entity_id, food_data.get("category"))
            if not result:
                success = False
                failure.append("category")

        if food_data.get("size"):
            total_values += 1
            result = core.update.food_size(entity_id, food_data.get("size"))
            if not result:
                success = False
                failure.append("size")

        if success:
            return {"success": True, "message": "", "code": 0, "data": {}}

        if len(failure) == total_values:
            raise EntryNotFound

        raise DataInconsistencyError

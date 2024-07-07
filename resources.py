from flask_restful import Resource
from flask import request
from errors import EntryNotFound, MissingFoodSize, DataInconsistencyError, MissingFoodData
from core import Controller
import logging

class ManageFood(Resource):
    def __init__(self, core: Controller):
        self.core = core

    def get(self, entity_id):
        entity = self.core.find_food(entity_id)
        if entity:
            return {
                "success": True,
                "message": "",
                "code": 0,
                "data": entity
            }
        else:
            raise EntryNotFound

    def delete(self, entity_id):
        try:
            food = self.core.delete_food(entity_id)
        except:
            raise EntryNotFound
        return {
            "success": True,
            "message": "",
            "code": 0,
            "data": food
        }

    def put(self, entity_id):
        data = request.get_json()
        if not data.get("food"):
            raise MissingFoodData
        food_data = data.get("food")

        food_entity = self.core.find_food(entity_id)
        if not food_entity:
            raise EntryNotFound

        food = self.core.update_food_name(entity_id, data.get("food"))

        if not food:
            logging.error("Food entity exists, but when attempted to be updated, the entity was not found.")
            logging.error(f"Entity ID: {entity_id}\nData: {data}")
            raise DataInconsistencyError

        food_data = data.get("food")

        if not food_data:
            raise MissingFoodData

        failure = []
        total_values = 0
        success = True

        if food_data.get("food_name"):
            print(food_data.get("food_name"))
            total_values += 1
            result = self.core.update_food_name(entity_id, food_data.get("food_name"))
            if not result:
                success = False
                failure.append("food_name")

        if food_data.get("price"):
            total_values += 1
            result = self.core.update_food_price(entity_id, food_data.get("price"))
            if not result:
                success = False
                failure.append("price")

        if food_data.get("category"):
            total_values += 1
            result = self.core.update_food_category(entity_id, food_data.get("category"))
            if not result:
                success = False
                failure.append("category")

        if food_data.get("food_size"):
            total_values += 1
            result = self.core.update_food_size(entity_id, food_data.get("food_size"))
            if not result:
                success = False
                failure.append("food_size")

        if success:
            return {
                "success": True, 
                "message": "", 
                "code": 0, 
                "data": {}
            }

        if len(failure) == total_values:
            raise EntryNotFound

        raise DataInconsistencyError

class CreateFood(Resource):
    def __init__(self, core: Controller):
        self.core = core

    def post(self):
        data = request.get_json()
        food_data = data.get("food")
        if not food_data or not {"food_name", "price", "category"} <= set(food_data):
            raise MissingFoodData
        food = self.core.create_food(
            food_data.get("food_name"),
            food_data.get("price"),
            food_data.get("category"),
            food_size=food_data.get("food_size")
        )
        if food:
            return {
                "success": True,
                "message": "",
                "code": 0,
                "data": food
            }
        else:
            raise MissingFoodSize

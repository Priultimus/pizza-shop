import logging

from flask_restful import Resource  # type: ignore
from flask import request, Response

from .helper import clean_data

from .. import core
from ..errors import (
    EntryNotFound,
    ImproperEntryData,
    DataInconsistencyError,
    MissingEntryData,
    PARTIAL_SUCCESS,
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
            float(food_data.get("price")),
            food_data.get("category"),
            food_size=food_data.get("size"),
        )
        if not food:
            raise ImproperEntryData("Food size is required for this category.")

        resp = clean_data(
            {"success": True, "message": "", "code": 0, "data": food}, serialize=True
        )
        headers = {"location": f"api/menu/food/{food['id']}"}
        return Response(resp, status=201, mimetype="application/json", headers=headers)


class ManageFood(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageFood")

    def get(self, food_id):
        food = core.find.food(food_id)
        if not food:
            raise EntryNotFound
        resp = clean_data(
            {"success": True, "message": "", "code": 0, "data": food}, serialize=True
        )
        return Response(resp, status=200, mimetype="application/json")

    def delete(self, food_id):
        food = core.delete.food(food_id)
        if not food:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}, 204

    def put(self, food_id):
        data = request.get_json()
        food_data = data.get("food")
        if not food_data:
            raise MissingEntryData

        food_entity = core.find.food(food_id)
        if not food_entity:
            raise EntryNotFound

        attempted_entries = {}

        if food_data.get("name"):
            attempted_entries["name"] = True
            if not core.update.food_name(food_id, food_data.get("name")):
                attempted_entries["name"] = False

        if food_data.get("price"):
            attempted_entries["price"] = True
            if not core.update.food_price(food_id, float(food_data.get("price"))):
                attempted_entries["price"] = False

        if food_data.get("category"):
            attempted_entries["category"] = True
            if not core.update.food_category(food_id, food_data.get("category")):
                attempted_entries["category"] = False

        if food_data.get("size"):
            attempted_entries["size"] = True
            if not core.update.food_size(food_id, food_data.get("size")):
                attempted_entries["size"] = False

        if not len(attempted_entries):
            # no useful data was provided by the user
            raise ImproperEntryData

        data = core.find.food(food_id)
        success = all(attempted_entries.values())

        if not data:
            # between updating the data and fetching it again, it vanished!
            raise DataInconsistencyError

        if success:
            resp = clean_data(
                {"success": True, "message": "", "code": 0, "data": data},
                serialize=True,
            )
            return Response(resp, status=200, mimetype="application/json")

        resp = clean_data(
            {
                "success": False,
                "message": "Some items did not successfully update. ",
                "code": PARTIAL_SUCCESS,
                "data": data,
                "results": attempted_entries,
            },
            serialize=True,
        )

        return Response(resp, status=207, mimetype="application/json")

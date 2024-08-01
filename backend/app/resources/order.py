import json
import logging
from .helper import clean_data

from flask_restful import Resource  # type: ignore
from flask import request, Response

from .helper import clean_data

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    ImproperEntryData,
    MissingEntryData,
    PARTIAL_SUCCESS
)


class CreateOrder(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateOrder")

    def post(self, customer_id):
        customer = core.find.customer(customer_id)
        if not customer:
            raise EntryNotFound("This customer does not exist.")
        data: dict = request.get_json()
        order_data: dict = data.get("order")
        order_item_data: dict = data.get("items")
        order_item_data = {int(k): v for k, v in order_item_data.items()}
        if not order_data or not order_item_data or not {"payment_method", "type"} <= set(order_data):
            raise MissingEntryData
        order = core.create.order(
            #order_data.get("customer_id"),
            customer_id,
            order_item_data,
            order_data.get("payment_method"),
            order_data.get("type"),
        )
        if not order:
            raise ImproperEntryData("The order could not be created.")
        data = clean_data({"success": True, "message": "", "code": 0, "data": order}, serialize=True)
        headers = {"location": f"api/customer/{customer_id}/order/{order['order_id']}"}
        return Response(data, status=201, mimetype="application/json", headers=headers)

class ManageOrder(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageOrder")
    
    def get(self, entity_id):
        order = core.find.order(entity_id)
        if not order:
            raise EntryNotFound
        resp = clean_data({"success": True, "message": "", "code": 0, "data": order}, serialize=True)
        return Response(resp, status=200, mimetype="application/json")

    def delete(self, entity_id):
        order = core.delete.order(entity_id)
        if not order:
            raise EntryNotFound
        return {
            "success": True, 
            "message": "", 
            "code": 0, 
            "data": {}
            }, 204
    
    def put(self, entity_id):
        data = request.get_json()
        order_data = data.get("order")
        if not order_data:
            raise MissingEntryData
        
        order_entity = core.find.order(entity_id)
        if not order_entity:
            raise EntryNotFound
        
        attempted_entries = {}

        if order_data.get("customer_id"):
            attempted_entries["customer_id"] = True
            if not core.update.order_customer(entity_id, order_data.get("customer_id")):
                attempted_entries["customer_id"] = False

        if order_data.get("payment_method"):
            attempted_entries["payment_method"] = True
            if not core.update.order_payment_method(entity_id, order_data.get("payment_method")):
                attempted_entries["payment_method"] = False
        
        if order_data.get("order_type"):
            attempted_entries["order_type"] = True
            if not core.update.order_type(entity_id, order_data.get("order_type")):
                attempted_entries["order_type"] = False
        
        if order_data.get("order_items"):
            attempted_entries["order_items"] = True
            if not core.update.order_items(entity_id, order_data.get("order_items")):
                attempted_entries["order_items"] = False

        if not len(attempted_entries): 
            # no useful data was provided by the user
            raise ImproperEntryData

        data = core.find.order(entity_id) # fetch updated data
        success = all(attempted_entries.values())

        if not data: 
            # between updating the data and fetching it again, it vanished!
            raise DataInconsistencyError

        if success:
            resp = clean_data({"success": True, "message": "", "code": 0, "data": data}, serialize=True)
            return Response(resp, status=200, mimetype="application/json")

        resp = clean_data({
            "success": False, 
            "message": "Some items did not successfully update. ", 
            "code": PARTIAL_SUCCESS, 
            "data": data, 
            "results": attempted_entries}, serialize=True
            )

        return Response(resp, status=207, mimetype="application/json")

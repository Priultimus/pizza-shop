import logging

from copy import deepcopy

from flask_restful import Resource  # type: ignore
from flask import request, Response

from .helper import clean_data

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    MissingEntryData,
    ImproperEntryData,
    PARTIAL_SUCCESS,
)


class CreateCustomer(Resource):
    def __init__(self):
        self.logger = logging.getLogger("CreateCustomer")

    def post(self):
        data = request.get_json()
        customer_data = data.get("customer")
        if not (
            customer_data
            or {"name", "address", "phone"} <= set(customer_data)
            or {"street", "city", "province", "postal_code"}
            <= set(customer_data.get("address"))
        ):
            raise MissingEntryData
        customer = core.create.customer(
            customer_data.get("name"),
            customer_data.get("phone"),
            customer_data.get("address"),
        )
        resp = clean_data(
            {"success": True, "message": "", "code": 0, "data": customer},
            serialize=True,
        )
        headers = {"location": f"api/customer/{customer['id']}"}
        return Response(resp, status=201, mimetype="application/json", headers=headers)


class ManageCustomer(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageCustomer")

    def get(self, customer_id: int):
        customer = core.find.customer(customer_id)
        if not customer:
            raise EntryNotFound
        resp = clean_data(
            {"success": True, "message": "", "code": 0, "data": customer},
            serialize=True,
        )
        return Response(resp, status=200, mimetype="application/json")

    def delete(self, customer_id: int):
        customer = core.delete.customer(customer_id)
        if not customer:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}, 204

    def put(self, customer_id: int):
        data = request.get_json()
        customer_data = data.get("customer")
        if not customer_data:
            raise MissingEntryData

        customer_entity = core.find.customer(customer_id)
        if not customer_entity:
            raise EntryNotFound

        attempted_entries = {}

        if customer_data.get("name"):
            attempted_entries["name"] = True
            if not core.update.customer_name(customer_id, customer_data.get("name")):
                attempted_entries["name"] = False

        if customer_data.get("phone"):
            attempted_entries["phone"] = True
            if not core.update.customer_phone(customer_id, customer_data.get("phone")):
                attempted_entries["phone"] = False

        if customer_data.get("address"):
            attempted_entries["address"] = True
            if not core.update.customer_address(
                customer_id, customer_data.get("address")
            ):
                attempted_entries["address"] = False

        if not len(attempted_entries):
            # no useful data was provided by the user
            raise ImproperEntryData

        data = core.find.customer(customer_id)
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

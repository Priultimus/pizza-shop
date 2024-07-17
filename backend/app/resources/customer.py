import logging

from flask_restful import Resource  # type: ignore
from flask import request

from .. import core
from ..errors import (
    EntryNotFound,
    DataInconsistencyError,
    MissingEntryData,
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
        return {"success": True, "message": "", "code": 0, "data": customer}


class ManageCustomer(Resource):
    def __init__(self):
        self.logger = logging.getLogger("ManageCustomer")

    def get(self, customer_id: int):
        customer = core.find.customer(customer_id)
        if not customer:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": customer}

    def delete(self, customer_id: int):
        customer = core.delete.customer(customer_id)
        if not customer:
            raise EntryNotFound
        return {"success": True, "message": "", "code": 0, "data": {}}

    def put(self, customer_id: int):
        data = request.get_json()
        customer_data = data.get("customer")
        if not customer_data:
            raise MissingEntryData

        customer_entity = core.find.customer(customer_id)
        if not customer_entity:
            raise EntryNotFound

        failure = []
        total_values = 0
        success = True

        if customer_data.get("name"):
            total_values += 1
            if not core.update.customer_name(customer_id, customer_data.get("name")):
                failure.append("name")
                success = False

        if customer_data.get("phone"):
            total_values += 1
            if not core.update.customer_phone(customer_id, customer_data.get("phone")):
                failure.append("phone")
                success = False

        if customer_data.get("address"):
            total_values += 1
            if not core.update.customer_address(
                customer_id, customer_data.get("address")
            ):
                failure.append("address")
                success = False

        if not total_values:
            raise MissingEntryData

        if len(failure) == total_values:
            raise EntryNotFound

        data = core.find.customer(customer_id)

        if success and data:
            return {"success": True, "message": "", "code": 0, "data": data}

        raise DataInconsistencyError

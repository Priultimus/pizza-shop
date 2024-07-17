import logging
from typing import Union

from . import find

from ..database import ManageResturantData, ViewResturantData
from ..errors import EntityNotFound


class Delete:
    def __init__(self):
        self.manager = ManageResturantData()
        self.viewer = ViewResturantData()
        self.logger = logging.getLogger("core.delete")

    def food(self, food_id: int) -> bool:
        try:
            self.manager.remove_food(food_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred deleting the food item.")
            self.logger.warning(f"Food ID: {food_id}")
            raise

        return True

    def addon(self, addon_id: int) -> bool:
        try:
            self.manager.remove_addon(addon_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred deleting the addon item.")
            self.logger.warning(f"Addon ID: {addon_id}")
            raise

        return True

    def customer(self, customer_id: int) -> bool:
        try:
            self.manager.remove_customer(customer_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred deleting the customer.")
            self.logger.warning(f"Customer ID: {customer_id}")
            raise
        return True

    def order(self, order_id: int) -> bool:
        try:
            self.manager.remove_order(order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred deleting the order.")
            self.logger.warning(f"Order ID: {order_id}")
            raise

        return True

    def order_item(
        self, order_id: int, order_item_id: int, query_order=False
    ) -> Union[dict, bool]:
        try:
            order = self.viewer.view_order(order_id)
        except EntityNotFound:
            return False

        price = order.convert_to_dict().get("order_price")
        try:
            order_item_price = (
                self.viewer.view_order_item(order_item_id)
                .convert_to_dict()
                .get("price")
            )
        except EntityNotFound:
            return False

        price -= order_item_price
        self.manager.remove_order_item(order_item_id)
        self.manager.update_order(order_id, order_price=price)

        if query_order:
            return find.order(order_id)

        return True

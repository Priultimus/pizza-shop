import logging
from typing import Union

from ..database import ManageResturantData, ViewResturantData
from ..errors import EntityNotFound


class Find:
    def __init__(self):
        self.manager = ManageResturantData()
        self.viewer = ViewResturantData()
        self.logger = logging.getLogger("core.find")

    def food(self, food_id: int) -> Union[dict, bool]:
        try:
            food = self.viewer.view_food(food_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred searching for a food item."
            )
            self.logger.warning(f"Food ID: {food_id}")
            raise

        return food.convert_to_dict()

    def addon(self, addon_id: int) -> Union[dict, bool]:
        try:
            addon = self.viewer.view_addon(addon_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred searching for an addon item."
            )
            self.logger.warning(f"Addon ID: {addon_id}")
            raise

        return addon.convert_to_dict()

    def customer(self, customer_id: int) -> Union[dict, bool]:
        try:
            customer = self.viewer.view_customer(customer_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred searching for a customer.")
            self.logger.warning(f"Customer ID: {customer_id}")
            raise

        return customer.convert_to_dict()

    def order(self, order_id: int) -> Union[dict, bool]:
        try:
            order = self.viewer.view_order(order_id)
            order_price = self.viewer.view_order_grand_total(order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred searching for an order.")
            self.logger.warning(f"Order ID: {order_id}")
            raise
        try:
            order_items = self.viewer.view_order_items(order_id)
        except EntityNotFound:
            order_items = []
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred looking for order items while searching for an order."
            )
            self.logger.warning(f"Order ID: {order_id}")
            raise

        orderitems = []
        for order_item in order_items:
            item_mods = self.viewer.view_item_mods(order_item.order_item_id)
            orderitem = order_item.convert_to_dict()
            orderitem["addons"] = [item_mod.convert_to_dict() for item_mod in item_mods]
            orderitems.append(orderitem)

        order = order.convert_to_dict()
        order["order_items"] = orderitems
        order["order_price"] = order_price
        order["customer_id"] = self.viewer.view_order_customer(order_id).customer_id

        return order

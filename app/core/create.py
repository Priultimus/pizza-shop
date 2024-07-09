import logging
from datetime import datetime
from typing import Union

from ..database import ManageResturantData, ViewResturantData
from ..errors import ResturantException, CustomerNotFoundError


class Create:
    def __init__(self):
        self.manager = ManageResturantData()
        self.viewer = ViewResturantData()
        self.logger = logging.getLogger("core.create")

    def food(
        self, food_name: str, price: int, category: str, food_size=None
    ) -> Union[dict, bool]:
        try:
            food = self.manager.new_food_item(
                food_name, price, category, food_size=food_size
            )
        except ResturantException:
            self.logger.debug(
                f"Attempted to create a new food item with a category that requires a new food size."
            )
            self.logger.debug(
                f"Name: {food_name} Price: {price} Category: {category} Food Size: {food_size}"
            )
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred creating a new food item.")
            self.logger.warning(
                f"Name: {food_name} Price: {price} Category: {category} Food Size: {food_size}"
            )
            raise

        return food.convert_to_dict()

    def addon(
        self, addon_name: str, addon_type: str, addon_price, addon_size=None
    ) -> dict:
        try:
            addon = self.manager.new_addon_item(
                addon_name, addon_type, addon_price, addon_size=addon_size
            )
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred creating a new addon item."
            )
            self.logger.warning(
                f"Name: {addon_name} Price: {addon_price} Addon Size: {addon_size}"
            )
            raise

        return addon.convert_to_dict()

    def customer(
        self, customer_name: str, customer_phone: int, customer_address: dict = {}
    ) -> dict:
        try:
            customer = self.manager.new_customer(
                customer_name,
                customer_phone,
                customer_street=customer_address.get("street"),
                customer_city=customer_address.get("city"),
                customer_province=customer_address.get("province"),
                customer_postal_code=customer_address.get("postal_code"),
            )
        except Exception as e:
            self.logger.warning("An unhandled error occurred creating a new customer.")
            self.logger.warning(
                f"Name: {customer_name} Phone: {customer_phone} Address: {customer_address}"
            )
            self.logger.warning(
                f"Customer Street: {customer_address.get('street')} Customer City: {customer_address.get('city')}"
            )
            self.logger.warning(
                f"Customer Province: {customer_address.get('province')} Customer Postal Code: {customer_address.get('postal_code')}"
            )
            raise

        return customer.convert_to_dict()

    def order(
        self,
        customer_id: int,
        order_items: dict,
        payment_method: str,
        order_type: str,
    ) -> Union[dict, bool]:
        order = self.manager.new_order(datetime.now(), payment_method, order_type)
        customer = self.viewer.view_customer(customer_id)
        if not customer:
            return False
        order_id = order.order_id
        self.manager.new_customer_order(customer_id, order_id)
        orderitems = []
        order_price = 0
        for food_id in order_items:
            food = self.viewer.view_food(food_id)
            food_addons = order_items[food_id]
            order_item = self.manager.new_order_item(order_id, food_id, food.price)
            order_item_id = order_item.order_item_id

            order_price += food.price
            addons = []
            for addon_id in food_addons:
                addon = self.viewer.view_addon(addon_id)
                addons.append(addon.convert_to_dict())
                order_price += addon.price
                self.manager.new_item_mod(order_item_id, addon_id, 0, addon.price)
            orderitem = order_item.convert_to_dict()
            orderitem["addons"] = addons
            orderitems.append(orderitems)

        order = order.convert_to_dict()
        order["order_price"] = order_price
        order["customer_id"] = customer_id
        order["order_items"] = orderitems

        return order

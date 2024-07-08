import logging

from datetime import datetime
from typing import Union

from ..database import ManageResturantData, ViewResturantData
from ..errors import EntityNotFound


class Update:
    def __init__(self):
        self.manager = ManageResturantData()
        self.viewer = ViewResturantData()
        self.logger = logging.getLogger("core.update")

    def food_name(self, food_id: int, food_name: str) -> bool:
        try:
            self.manager.update_food(food_id, food_name=food_name)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the food item name."
            )
            self.logger.warning(f"Food ID: {food_id} New Name: {food_name}")
            raise

        return True

    def food_price(self, food_id: int, price: int) -> bool:
        try:
            self.manager.update_food(food_id, price=price)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the food item price."
            )
            self.logger.warning(f"Food ID: {food_id} New Price: {price}")
            raise

        return True

    def food_category(self, food_id: int, category: str) -> bool:
        try:
            self.manager.update_food(food_id, category=category)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the food item category."
            )
            self.logger.warning(f"Food ID: {food_id} New Category: {category}")
            raise

        return True

    def food_size(self, food_id: int, food_size: str) -> bool:
        try:
            self.manager.update_food(food_id, food_size=food_size)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the food item size."
            )
            self.logger.warning(f"Food ID: {food_id} New Size: {food_size}")
            raise

        return True

    def addon_name(self, addon_id: int, addon_name: str) -> bool:
        try:
            self.manager.update_addon(addon_id, addon_name=addon_name)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the addon item name."
            )
            self.logger.warning(f"Addon ID: {addon_id} New Name: {addon_name}")
            raise

        return True

    def addon_type(self, addon_id: int, addon_type: str) -> bool:
        try:
            self.manager.update_addon(addon_id, addon_type=addon_type)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the addon item type."
            )
            self.logger.warning(f"Addon ID: {addon_id} New Type: {addon_type}")
            raise

    def addon_price(self, addon_id: int, price: int) -> bool:
        try:
            self.manager.update_addon(addon_id, price=price)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the addon item price."
            )
            self.logger.warning(f"Addon ID: {addon_id} New Price: {price}")
            raise

        return True

    def addon_size(self, addon_id: int, addon_size: str) -> bool:
        try:
            self.manager.update_addon(addon_id, addon_size=addon_size)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the addon item size."
            )
            self.logger.warning(f"Addon ID: {addon_id} New Size: {addon_size}")
            raise

        return True

    def customer_name(self, customer_id: int, name: str) -> bool:
        try:
            self.manager.update_customer(customer_id, name=name)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer name."
            )
            self.logger.warning(f"Customer ID: {customer_id} New Name: {name}")
            raise

        return True

    def customer_phone(self, customer_id: int, phone: int) -> bool:
        try:
            self.manager.update_customer(customer_id, phone=phone)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer phone."
            )
            self.logger.warning(f"Customer ID: {customer_id} New Phone: {phone}")
            raise

        return True

    def customer_address(self, customer_id: int, customer_address: dict) -> bool:
        try:
            self.manager.update_customer(
                customer_id,
                customer_stress=customer_address.get("street"),
                customer_city=customer_address.get("city"),
                customer_province=customer_address.get("province"),
                customer_postal_code=customer_address.get("postal_code"),
            )
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer address."
            )
            self.logger.warning(
                f"Customer ID: {customer_id} Address: {customer_address}"
            )
            self.logger.warning(
                f"Customer Street: {customer_address.get('street')} Customer City: {customer_address.get('city')}"
            )
            self.logger.warning(
                f"Customer Province: {customer_address.get('province')} Customer Postal Code: {customer_address.get('postal_code')}"
            )
            raise

        return True

    def customer_street(self, customer_id: int, street: str) -> bool:
        try:
            self.manager.update_customer(customer_id, customer_stress=street)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer street."
            )
            self.logger.warning(f"Customer ID: {customer_id} New Street: {street}")
            raise

        return True

    def customer_city(self, customer_id: int, city: str) -> bool:
        try:
            self.manager.update_customer(customer_id, customer_city=city)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer city."
            )
            self.logger.warning(f"Customer ID: {customer_id} New City: {city}")
            raise

        return True

    def customer_province(self, customer_id: int, province: str) -> bool:
        try:
            self.manager.update_customer(customer_id, customer_province=province)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer province."
            )
            self.logger.warning(f"Customer ID: {customer_id} New Province: {province}")
            raise

        return True

    def customer_postal_code(self, customer_id: int, postal_code: str) -> bool:
        try:
            self.manager.update_customer(customer_id, customer_postal_code=postal_code)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the customer postal code."
            )
            self.logger.warning(
                f"Customer ID: {customer_id} New Postal Code: {postal_code}"
            )
            raise

        return True

    def order_payment_method(
        self, order_id: int, payment_method: str, query_order=False
    ) -> bool:
        try:
            self.manager.update_order(
                order_id, payment_method=payment_method
            ).convert_to_dict()
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred updating the order payment method."
            )
            self.logger.warning(
                f"Order ID: {order_id} New Payment Method: {payment_method}"
            )
            raise

        if query_order:
            return self.find(order_id)

        return True

    def order_type(
        self, order_id: int, order_type: str, query_order=False
    ) -> Union[dict, bool]:
        try:
            order = self.manager.update_order(order_id, order_type=order_type)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred updating the order type.")
            self.logger.warning(f"Order ID: {order_id} New Type: {order_type}")
            raise

        if query_order:
            return self.find(order_id)

        return True

    def order_customer(
        self, order_id: int, customer_id: int, query_order=False
    ) -> Union[dict, bool]:
        try:
            self.manager.remove_customer_order(customer_id, order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred removing the old order customer."
            )
            self.logger.warning(f"Order ID: {order_id} Customer ID: {customer_id}")
            raise

        try:
            customer_order = self.manager.new_customer_order(customer_id, order_id)
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred creating the new order customer."
            )
            self.logger.warning(f"Order ID: {order_id} Customer ID: {customer_id}")
            raise

        if query_order:
            return self.find(order_id)

        return True

    def order_item(
        self, order_item_id: int, food_id: int, price: int, query_order=False
    ) -> bool:
        try:
            self.manager.update_order_item(order_item_id, food_id, price)
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning("An unhandled error occurred updating an order item.")
            self.logger.warning(
                f"Order Item ID: {order_item_id} Food ID: {food_id} Price: {price}"
            )
            raise

        if query_order:
            order_id = self.viewer.view_order_item(order_item_id).order_id
            return self.find(order_id)

        return True

    def order_items(
        self, order_id: int, order_items: dict, query_order=False
    ) -> Union[dict, bool]:
        try:
            order = self.viewer.view_food(order_id).convert_to_dict()
        except EntityNotFound:
            return False
        except Exception as e:
            self.logger.warning(
                "An unhandled error occurred finding the order to add a new order item."
            )
            self.logger.warning(f"Order ID: {order_id}")
            raise

        orderitems = []
        addons = []
        for food_id in order_items:
            food = self.viewer.view_food(food_id).convert_to_dict()
            food_addons = order_items[food_id]
            order_item = self.manager.new_order_item(
                order.get("order_id"), food_id, food.get("price")
            )
            orderitems.append(order_item.convert_to_dict())
            for addon_id in food_addons:
                addon = self.viewer.view_addon(addon_id)
                addon_price = addon["price"]
                addons.append(addon.convert_to_dict())
                self.manager.new_item_mod(
                    order_item.get("order_item_id"), addon_id, 1, addon_price
                )

        if query_order:
            return self.find(order_id)

        return True

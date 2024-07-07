import logging
from datetime import datetime
from typing import Union, Optional as optional

from sqlalchemy.exc import IntegrityError
from models import Customer, MySQLBackend, ManageResturantData, ViewResturantData
from errors import ResturantException, EntityNotFound

def handle_session(f):
    """Decorator function to handle session."""
    def wrapper(self, *args, **kwargs):
        session = self.Session()
        try:
            result = f(self, session, *args, **kwargs)
            return result
        except IntegrityError:
            session.rollback()
            raise Exception("Error")
        finally:
            session.expunge_all()
            session.close()  
    return wrapper

class CoreError(Exception):
    pass

class CustomerNotFoundError(CoreError):
    pass

class Controller(MySQLBackend):
    """Controller class that inherits from MySQLBackend."""

    def __init__(self, db_url):
        super(Controller, self).__init__(db_url)
        self.customer = Customer()
        self.manager = ManageResturantData()
        self.viewer = ViewResturantData()

    
    @handle_session
    def find_food(self, session, food_id: int) -> Union[dict, bool]:
        try:
            food = self.viewer.view_food(session, food_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred searching for a food item.")
            logging.warning(f"Food ID: {food_id}")
            logging.error(e)
            raise

        return food.convert_to_dict()
 
    @handle_session
    def create_food(self, session, food_name: str, price: int, category: str, food_size=None) -> Union[dict, bool]:
        try:
            food = self.manager.new_food_item(session, 
                                          food_name,
                                          price, 
                                          category, 
                                          food_size=food_size
                                          )
        except ResturantException:
            logging.debug(f"Attempted to create a new food item with a category that requires a new food size.") 
            logging.debug(f"Name: {food_name}\nPrice: {price}\nCategory: {category}\nFood Size: {food_size}")
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred creating a new food item.")
            logging.warning(f"Name: {food_name}\nPrice: {price}\nCategory: {category}\nFood Size: {food_size}")
            logging.error(e)
            raise
        return food.convert_to_dict()

    @handle_session
    def update_food_name(self, session, food_id: int, food_name: str) -> Union[dict, bool]:
        try:
            food = self.manager.update_food(session, food_id, food_name=food_name)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the food item name.")
            logging.warning(f"Food ID: {food_id}\nNew Name: {food_name}")
            logging.error(e)
            raise

        return food.convert_to_dict()
    
    @handle_session
    def update_food_price(self, session, food_id: int, price: int) -> Union[dict, bool]:
        try:
            food = self.manager.update_food(session, food_id, price=price)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the food item price.")
            logging.warning(f"Food ID: {food_id}\nNew Price: {price}")
            logging.error(e)
            raise

        return food.convert_to_dict()
    
    @handle_session
    def update_food_category(self, session, food_id: int, category: str) -> Union[dict, bool]:
        try:
            food = self.manager.update_food(session, food_id, category=category)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the food item category.")
            logging.warning(f"Food ID: {food_id}\nNew Category: {category}")
            logging.error(e)
            raise

        return food.convert_to_dict()
    
    @handle_session
    def update_food_size(self, session, food_id: int, food_size: str) -> Union[dict, bool]:
        try:
            food = self.manager.update_food(session, food_id, food_size=food_size)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the food item size.")
            logging.warning(f"Food ID: {food_id}\nNew Size: {food_size}")
            logging.error(e)
            raise

        return food.convert_to_dict()
    
    @handle_session
    def delete_food(self, session, food_id: int) -> bool:
        try:
            self.manager.remove_food(session, food_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred deleting the food item.")
            logging.warning(f"Food ID: {food_id}")
            logging.error(e)
            raise

        return True

    @handle_session
    def find_addon(self, session, addon_id: int) -> Union[dict, bool]:
        try:
            addon = self.viewer.view_addon(session, addon_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred searching for an addon item.")
            logging.warning(f"Addon ID: {addon_id}")
            logging.error(e)
            raise

        return addon.convert_to_dict()

    @handle_session
    def create_addon(self, session, addon_name: str, addon_type: str, price, addon_size=None):
        try:
            addon = self.manager.new_addon_item(session, addon_name, addon_type, price, addon_size=addon_size)
        except Exception as e:
            logging.warning("An unhandled error occurred creating a new addon item.")
            logging.warning(f"Name: {addon_name}\nPrice: {price}\nAddon Size: {addon_size}")
            logging.error(e)
            raise
        return addon.convert_to_dict()
    
    @handle_session
    def update_addon_name(self, session, addon_id: int, addon_name: str) -> Union[dict, bool]:
        try:
            addon = self.manager.update_addon(session, addon_id, addon_name=addon_name)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the addon item name.")
            logging.warning(f"Addon ID: {addon_id}\nNew Name: {addon_name}")
            logging.error(e)
            raise

        return addon.convert_to_dict()
    
    @handle_session
    def update_addon_price(self, session, addon_id: int, price: int) -> Union[dict, bool]:
        try:
            addon = self.manager.update_addon(session, addon_id, price=price)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the addon item price.")
            logging.warning(f"Addon ID: {addon_id}\nNew Price: {price}")
            logging.error(e)
            raise

        return addon.convert_to_dict()
    
    @handle_session
    def update_addon_size(self, session, addon_id: int, addon_size: str) -> Union[dict, bool]:
        try:
            addon = self.manager.update_addon(session, addon_id, addon_size=addon_size)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the addon item size.")
            logging.warning(f"Addon ID: {addon_id}\nNew Size: {addon_size}")
            logging.error(e)
            raise

        return addon.convert_to_dict()
    
    @handle_session
    def delete_addon(self, session, addon_id: int) -> bool:
        try:
            self.manager.remove_addon(session, addon_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred deleting the addon item.")
            logging.warning(f"Addon ID: {addon_id}")
            logging.error(e)
            raise

        return True
    
    @handle_session
    def find_customer(self, session, customer_id: int) -> Union[dict, bool]:
        try:
            customer = self.viewer.view_customer(session, customer_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred searching for a customer.")
            logging.warning(f"Customer ID: {customer_id}")
            logging.error(e)
            raise

        return customer.convert_to_dict()

    @handle_session
    def create_customer(self, session, 
                        name: str, 
                        phone: int, 
                        customer_address: dict={}
                        ) -> dict:
        try:
            customer = self.manager.new_customer(session, 
                                             name, 
                                             phone, 
                                             customer_street=customer_address.get("street"), 
                                             customer_city=customer_address.get("city"), 
                                             customer_province=customer_address.get("province"), 
                                             customer_postal_code=customer_address.get("postal_code")
                                             )
        except Exception as e:
            logging.warning("An unhandled error occurred creating a new customer.")
            logging.warning(f"Name: {name}\nPhone: {phone}\nAddress: {customer_address}")
            logging.warning(f"Customer Street: {customer_address.get('street')}\nCustomer City: {customer_address.get('city')}")
            logging.warning(f"Customer Province: {customer_address.get('province')}\nCustomer Postal Code: {customer_address.get('postal_code')}")
            logging.error(e)
            raise
        
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_name(self, session, customer_id: int, name: str) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, name=name)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer name.")
            logging.warning(f"Customer ID: {customer_id}\nNew Name: {name}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_phone(self, session, customer_id: int, phone: int) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, phone=phone)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer phone.")
            logging.warning(f"Customer ID: {customer_id}\nNew Phone: {phone}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_address(self, session, customer_id: int, customer_address: dict) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, 
                                                 customer_id, 
                                                 customer_stress=customer_address.get("street"), 
                                                 customer_city=customer_address.get("city"), 
                                                 customer_province=customer_address.get("province"), 
                                                 customer_postal_code=customer_address.get("postal_code")
                                                 )
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer address.")
            logging.warning(f"Customer ID: {customer_id}\nAddress: {customer_address}")
            logging.warning(f"Customer Street: {customer_address.get('street')}\nCustomer City: {customer_address.get('city')}")
            logging.warning(f"Customer Province: {customer_address.get('province')}\nCustomer Postal Code: {customer_address.get('postal_code')}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_street(self, session, customer_id: int, street: str) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, customer_stress=street)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer street.")
            logging.warning(f"Customer ID: {customer_id}\nNew Street: {street}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_city(self, session, customer_id: int, city: str) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, customer_city=city)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer city.")
            logging.warning(f"Customer ID: {customer_id}\nNew City: {city}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_province(self, session, customer_id: int, province: str) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, customer_province=province)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer province.")
            logging.warning(f"Customer ID: {customer_id}\nNew Province: {province}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def update_customer_postal_code(self, session, customer_id: int, postal_code: str) -> Union[dict, bool]:
        try:
            customer = self.manager.update_customer(session, customer_id, customer_postal_code=postal_code)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the customer postal code.")
            logging.warning(f"Customer ID: {customer_id}\nNew Postal Code: {postal_code}")
            logging.error(e)
            raise
        return customer.convert_to_dict()
    
    @handle_session
    def delete_customer(self, session, customer_id: int) -> bool:
        try:
            self.manager.remove_customer(session, customer_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred deleting the customer.")
            logging.warning(f"Customer ID: {customer_id}")
            logging.error(e)
            raise
        return True
    
    @handle_session
    def find_order(self, session, order_id: int) -> Union[dict, bool]:
        try:
            order = self.viewer.view_order(session, order_id)
            order_price = self.viewer.view_order_grand_total(session, order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred searching for an order.")
            logging.warning(f"Order ID: {order_id}")
            logging.error(e)
            raise
        try:
            order_items = self.viewer.view_order_items(session, order_id)
        except EntityNotFound:
             order_items = []
        except Exception as e:
            logging.warning("An unhandled error occurred looking for order items while searching for an order.")
            logging.warning(f"Order ID: {order_id}")
            logging.error(e)
            raise

        orderitems = []
        for order_item in order_items:
            item_mods = self.viewer.view_item_mods(session, order_item.order_item_id)
            orderitem = order_item.convert_to_dict()
            orderitem["addons"] = [item_mod.convert_to_dict() for item_mod in item_mods]
            orderitems.append(orderitem)

        order = order.convert_to_dict()
        order["order_items"] = orderitems
        order["order_price"] = order_price
        order["customer_id"] = self.viewer.view_order_customer(session, order_id).customer_id

        return order

    @handle_session
    def create_order(self, session, 
                  customer_id: int, 
                  order_items: dict, 
                  payment_method: str, 
                  order_type: str,
                  ) -> dict:
        order = self.manager.new_order(session, datetime.now(), payment_method, order_type)
        customer = self.viewer.view_customer(session, customer_id)
        if not customer:
            raise CustomerNotFoundError(f"The customer \"{customer_id}\" does not exist.")
        order_id = order.order_id
        customer_order = self.manager.new_customer_order(session, customer_id, order_id)
        orderitems = []
        order_price = 0
        for food_id in order_items:
            food = self.viewer.view_food(session, food_id)
            food_addons = order_items[food_id]
            order_item = self.manager.new_order_item(session, order_id, food_id, food.price)
            order_item_id = order_item.order_item_id
            
            order_price += food.price
            addons = []
            for addon_id in food_addons:
                addon = self.viewer.view_addon(session, addon_id)
                addons.append(addon.convert_to_dict())
                order_price += addon.price
                self.manager.new_item_mod(session, order_item_id, addon_id, 0, addon.price)
            orderitem = order_item.convert_to_dict()
            orderitem["addons"] = addons
            orderitems.append(orderitems)

        order = order.convert_to_dict()
        order["order_price"] = order_price
        order["customer_id"] = customer_id
        order["order_items"] = orderitems

        return order

    @handle_session
    def update_order_payment_method(self, session, order_id: int, 
                              payment_method: str, 
                              query_order=False
                              ) -> Union[dict, bool]:
        try:
            order = self.manager.update_order(session, order_id, 
                                              payment_method=payment_method).convert_to_dict()
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the order payment method.")
            logging.warning(f"Order ID: {order_id}\nNew Payment Method: {payment_method}")
            logging.error(e)
            raise

        if query_order:
            return self.find(session, order_id)

        return True
    
    @handle_session
    def update_order_type(self, session, order_id: int, 
                          order_type: str, 
                          query_order=False
                          ) -> Union[dict, bool]:
        try:
            order = self.manager.update_order(session, order_id, order_type=order_type)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating the order type.")
            logging.warning(f"Order ID: {order_id}\nNew Type: {order_type}")
            logging.error(e)
            raise

        if query_order:
            return self.find(session, order_id)

        return True
    
    @handle_session
    def update_order_customer(self, session, order_id: int, 
                        customer_id: int, 
                        query_order=False
                        ) -> Union[dict, bool]:
        try:
            self.manager.remove_customer_order(session, customer_id, order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred removing the old order customer.")
            logging.warning(f"Order ID: {order_id}\nCustomer ID: {customer_id}")
            logging.error(e)
            raise

        try:
            customer_order = self.manager.new_customer_order(session, customer_id, order_id)
        except Exception as e:
            logging.warning("An unhandled error occurred creating the new order customer.")
            logging.warning(f"Order ID: {order_id}\nCustomer ID: {customer_id}")
            logging.error(e)
            raise

        if query_order:
            return self.find(session, order_id)

        return True
    
    @handle_session
    def add_order_items(self, session, order_id: int, 
                        order_items: dict, 
                        query_order=False
                        ) -> Union[dict, bool]:
        try:
            order = self.viewer.view_food(session, order_id).convert_to_dict()
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred finding the order to add a new order item.")
            logging.warning(f"Order ID: {order_id}")
            logging.error(e)
            raise
        orderitems = []
        addons = []
        for food_id in order_items:
            food = self.viewer.view_food(session, food_id).convert_to_dict()
            food_addons = order_items[food_id]
            order_item = self.manager.new_order_item(session, order.get("order_id"), food_id, food.get("price"))
            orderitems.append(order_item.convert_to_dict())
            for addon_id in food_addons:
                addon = self.viewer.view_addon(session, addon_id)
                addon_price = addon["price"]
                addons.append(addon.convert_to_dict())
                self.manager.new_item_mod(session, order_item.get("order_item_id"), addon_id, 1, addon_price)

        if query_order:
            return self.find(session, order_id)

        return True
    
    @handle_session
    def remove_order_item(self, session, order_id: int, 
                          order_item_id: int, 
                          query_order=False
                          ) -> Union[dict, bool]:
        try:
            order = self.viewer.view_order(session, order_id)
        except EntityNotFound:
            return False
        
        price = order.convert_to_dict().get("order_price")
        try:
            order_item_price = self.viewer.view_order_item(session, order_item_id).convert_to_dict().get("price")
        except EntityNotFound:
            return False
        
        price -= order_item_price
        self.manager.remove_order_item(session, order_item_id)
        self.manager.update_order(session, order_id, order_price=price)

        if query_order:
            return self.find(session, order_id)

        return True

    @handle_session
    def update_order_item(self, session, order_item_id: int, 
                          food_id: int, 
                          price: int, 
                          query_order=False
                          ) -> Union[dict, bool]:
        try:
            order_item = self.manager.update_order_item(session, order_item_id, food_id, price)
            order_id = order_item.order_id
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred updating an order item.")
            logging.warning(f"Order Item ID: {order_item_id}\nFood ID: {food_id}\nPrice: {price}")
            logging.error(e)
            raise

        if query_order:
            return self.find(session, order_id)

        return True
 
    @handle_session
    def delete_order(self, session, order_id: int) -> bool:
        try:
            self.manager.remove_order(session, order_id)
        except EntityNotFound:
            return False
        except Exception as e:
            logging.warning("An unhandled error occurred deleting the order.")
            logging.warning(f"Order ID: {order_id}")
            logging.error(e)
            raise

        return True

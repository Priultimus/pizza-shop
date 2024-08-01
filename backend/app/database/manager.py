from typing import Optional as optional

from sqlalchemy.inspection import inspect

from .. import db
from ..errors import ResturantException, EntityNotFound

from .models import Food, Addon, Customer, Order, CustomerOrder, OrderItem, ItemMod


class ManageResturantData:
    """This manages the creation, modification, and removal of menu items, customers and orders."""

    def __init__(self) -> None:
        self.food_size_required = ["pizza"]

    def new_food_item(
        self,
        food_name: str,
        food_price: int,
        food_category: str,
        food_size: optional[str] = None,
    ) -> Food:
        """Adds food items to the menu."""

        if food_category in self.food_size_required and not food_size:
            raise ResturantException("A size is required for this food type.")

        food_details = Food(
            food_name=food_name,
            food_category=food_category,
            food_price=food_price,
            food_size=food_size,
        )
        db.session.add(food_details)
        db.session.commit()
        return food_details

    def update_food(self, food_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given food item."""
        entity = Food.query.filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")

        required = [
            column.name for column in inspect(Food).c if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Food entity.\nThese are as follows:\n{'\n'.join(required)}"
            )

        if (
            any(attr in self.food_size_required for attr in kwargs)
            and not "food_size" in kwargs
        ):
            raise ResturantException("A size is required for this food type.")

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Food, req)] = kwargs.get(req)

        update = Food.query.filter(Food.food_id == food_id).update(
            update_dict, synchronize_session=False
        )
        db.session.commit()
        return update

    def remove_food(self, food_id: int) -> None:
        """Removes a food item from the menu."""
        entity = Food.query.filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return

    def new_addon_item(
        self,
        addon_name: str,
        addon_type: str,
        addon_price: int,
        addon_size: optional[str] = None,
    ) -> Addon:
        """Adds addon items to the menu."""

        if addon_type in self.food_size_required and not addon_size:
            raise ResturantException("A size is required for this addon type.")

        addon_details = Addon(
            addon_name=addon_name,
            addon_type=addon_type,
            addon_price=addon_price,
            addon_size=addon_size,
        )
        db.session.add(addon_details)
        db.session.commit()
        return addon_details

    def update_addon(self, addon_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given addon."""
        entity = Addon.query.filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")

        required = [
            column.name
            for column in inspect(Addon).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Addon entity. These are as follows:\n{'\n'.join(required)}"
            )

        if (
            any(attr in self.food_size_required for attr in kwargs)
            and not "addon_size" in kwargs
        ):
            raise ResturantException("A size is required for this addon type.")

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Addon, req)] = kwargs.get(req)

        update = Addon.query.filter(Addon.addon_id == addon_id).update(
            update_dict, synchronize_session=False
        )

        db.session.commit()
        return update

    def remove_addon(self, addon_id: int) -> None:
        """Removes an addon item from the menu."""
        entity = Addon.query.filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return

    def new_customer(
        self,
        customer_name: str,
        customer_phone_number: str,
        customer_street: optional[str] = None,
        customer_city: optional[str] = None,
        customer_province: optional[str] = None,
        customer_postal_code: optional[str] = None,
    ) -> Customer:
        """Adds customer details to the database."""
        customer_details = Customer(
            customer_name=customer_name,
            customer_phone_number=customer_phone_number,
            customer_street=customer_street,
            customer_city=customer_city,
            customer_province=customer_province,
            customer_postal_code=customer_postal_code,
        )
        db.session.add(customer_details)
        db.session.commit()
        return customer_details

    def update_customer(self, customer_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given customer."""
        entity = Customer.query.filter(Customer.customer_id == customer_id).first()
        if not entity:
            raise EntityNotFound("The customer does not exist in the database.")

        required = [
            column.name
            for column in inspect(Customer).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Customer entity.\nThese are as follows:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Customer, req)] = kwargs.get(req)

        update = Customer.query.filter(Customer.customer_id == customer_id).update(
            update_dict, synchronize_session=False
        )
        db.session.commit()
        return update

    def remove_customer(self, customer_id: int) -> None:
        """Removes a customer from the database."""
        entity = Customer.query.filter(Customer.customer_id == customer_id).first()
        if not entity:
            raise EntityNotFound("The customer does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return

    def new_order(
        self, order_date, order_payment_method: str, order_type: str
    ) -> Order:
        """Adds order details to the database."""
        order_details = Order(
            order_date=order_date,
            order_payment_method=order_payment_method,
            order_type=order_type,
        )
        db.session.add(order_details)
        db.session.commit()
        return order_details

    def update_order(self, order_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given order."""
        entity = Order.query.filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")

        required = [
            column.name
            for column in inspect(Order).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Order entity.\nThese are as follows:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Order, req)] = kwargs.get(req)

        update = Order.query.filter(Order.order_id == order_id).update(
            update_dict, synchronize_session=False
        )
        db.session.commit()
        return update

    def remove_order(self, order_id: int) -> None:
        """Removes an order from the database."""
        entity = Order.query.filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return

    def new_customer_order(self, customer_id: int, order_id: int) -> CustomerOrder:
        """Adds customer order details to the database."""
        customer_order_details = CustomerOrder(
            customer_id=customer_id, order_id=order_id
        )
        db.session.add(customer_order_details)
        db.session.commit()
        return customer_order_details

    def remove_customer_order(self, customer_id: int, order_id: int) -> None:
        """Removes a customer order from the database."""
        entity = (
            CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id)
            .filter(CustomerOrder.order_id == order_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The customer order does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return

    def remove_customer_orders(self, customer_id: int) -> None:
        """Removes all customer orders for a given customer."""
        entities = CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).all()
        if not entities:
            raise EntityNotFound("The customer does not have any orders.")
        for entity in entities:
            db.session.delete(entity)
        db.session.commit()
        return

    def new_order_item(
        self, order_id: int, food_id: int, order_item_price: int
    ) -> OrderItem:
        """Adds order item details to the database."""
        order_item_details = OrderItem(
            order_id=order_id, food_id=food_id, order_item_price=order_item_price
        )
        db.session.add(order_item_details)
        db.session.commit()
        return order_item_details

    def update_order_item(self, order_item_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given order item."""
        entity = OrderItem.query.filter(
            OrderItem.order_item_id == order_item_id
        ).first()
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")

        required = [
            column.name
            for column in inspect(OrderItem).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of OrderItem entity.\nThese are as follows:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(OrderItem, req)] = kwargs.get(req)

        update = OrderItem.query.filter(
            OrderItem.order_item_id == order_item_id
        ).update(update_dict, synchronize_session=False)
        db.session.commit()
        return update

    def remove_order_item(self, order_item_id: int) -> None:
        """Removes an order item from the database."""
        entity = OrderItem.query.filter(
            OrderItem.order_item_id == order_item_id
        ).first()
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")
        db.session.delete(entity)
        db.session.commit()
        return
    
    def remove_order_items(self, order_id: int) -> None:
        """Removes all order items for a given order."""
        entities = OrderItem.query.filter(OrderItem.order_id == order_id).all()
        if not entities:
            raise EntityNotFound("The order does not have any items.")
        for entity in entities:
            db.session.delete(entity)
        db.session.commit()

    def new_item_mod(
        self,
        order_item_id: int,
        addon_id: int,
        item_mod_qty: int,
        item_mod_price: int,
    ) -> ItemMod:
        """Adds item modification details to the database."""
        item_mod_details = ItemMod(
            order_item_id=order_item_id,
            addon_id=addon_id,
            item_mod_qty=item_mod_qty,
            item_mod_price=item_mod_price,
        )
        db.session.add(item_mod_details)
        db.session.commit()
        return item_mod_details

    def update_item_mod(self, order_item_id: int, addon_id: int, **kwargs) -> int:
        required = [
            column.name
            for column in inspect(ItemMod).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of ItemMod entity.\nThese are as follows:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(ItemMod, req)] = kwargs.get(req)

        update = (
            ItemMod.query.filter(ItemMod.order_item_id == order_item_id)
            .filter(ItemMod.addon_id == addon_id)
            .update(update_dict, synchronize_session=False)
        )
        db.session.commit()
        return update

    def remove_item_mod(self, order_item_id: int, addon_id: int) -> None:
        """Removes an item modification from the database."""
        entity = (
            ItemMod.query.filter(ItemMod.order_item_id == order_item_id)
            .filter(ItemMod.addon_id == addon_id)
            .first()
        )
        if not entity:
            raise EntityNotFound(
                "The item modification does not exist in the database."
            )
        db.session.delete(entity)
        db.session.commit()
        return
    
    def remove_item_mods(self, order_item_id: int) -> None:
        """Removes all item modifications for a given order item."""
        entities = ItemMod.query.filter(ItemMod.order_item_id == order_item_id).all()
        if not entities:
            raise EntityNotFound(
                "The order item does not have any modifications."
            )
        for entity in entities:
            db.session.delete(entity)
        db.session.commit()
        return

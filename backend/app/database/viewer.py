from sqlalchemy.orm.query import Query

from ..errors import EntityNotFound

from .models import Food, Addon, Customer, Order, OrderItem, ItemMod, CustomerOrder


class ViewResturantData:

    @staticmethod
    def view_food(food_id: int) -> Query:
        """Returns the details of a given food item."""
        entity = Food.query.filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")
        return entity

    @staticmethod
    def view_addon(addon_id: int) -> Query:
        """Returns the details of a given addon item."""
        entity = Addon.query.filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")
        return entity

    @staticmethod
    def view_customer(customer_id: int) -> Query:
        """Returns the details of a given customer."""
        entity = Customer.query.filter(Customer.customer_id == customer_id).first()
        if not entity:
            raise EntityNotFound(
                f'The customer "{customer_id}" does not exist in the database.'
            )
        return entity

    @staticmethod
    def view_customer_orders(customer_id: int) -> list[Query]:
        """Returns all orders for a given customer."""
        entities = CustomerOrder.query.filter(
            CustomerOrder.customer_id == customer_id
        ).all()
        if not entities:
            raise EntityNotFound("The customer does not have any orders.")
        return entities

    @staticmethod
    def view_order(order_id: int) -> Query:
        """Returns the details of a given order."""
        entity = Order.query.filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")
        return entity

    @staticmethod
    def view_order_grand_total(order_id: int) -> int:
        """Returns the grand total of a given order."""
        order_entity = Order.query.filter(Order.order_id == order_id).first()
        if not order_entity:
            raise EntityNotFound("The order does not exist in the database.")

        order_items = OrderItem.query.filter(OrderItem.order_id == order_id).all()
        total = 0
        # XXX: This *might* be incredibly slow. I have no idea, I've literally never written SQL before.
        for item in order_items:
            total += int(item.order_item_price)
            mod = ItemMod.query.filter(
                ItemMod.order_item_id == item.order_item_id
            ).all()
            for m in mod:
                total += int(m.item_mod_price)

        return total

    @staticmethod
    def view_order_customer(order_id: int) -> Query:
        """Returns the customer details for a given order."""
        entity = CustomerOrder.query.filter(CustomerOrder.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not have a customer.")
        return entity

    @staticmethod
    def view_order_item(order_item_id: int) -> Query:
        """Returns the details of a given order item."""
        entity = OrderItem.query.filter(
            OrderItem.order_item_id == order_item_id
        ).first()
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")
        return entity

    @staticmethod
    def view_order_items(order_id: int) -> list[Query]:
        """Returns the items in a given order."""
        order_items = OrderItem.query.filter(OrderItem.order_id == order_id).all()
        if not order_items:
            raise EntityNotFound("The order does not have any items.")
        return order_items

    @staticmethod
    def view_item_mods(order_item_id: int) -> list[Query]:
        """Returns all item modifications for a given order item."""
        entities = ItemMod.query.filter(ItemMod.order_item_id == order_item_id).all()
        if not entities:
            raise EntityNotFound("The order item does not have any modifications.")
        return entities

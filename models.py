import time
from typing import Optional as optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.orm.query import Query
from errors import ResturantException, EntityNotFound
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)


class MySQLBackend(object):
    """Represents MySQL backend that manages creating the engine and session."""

    def __init__(self, db_creation):
        self.engine = None
        self.Session = sessionmaker(autocommit=False, expire_on_commit=False)
        self.setup_engine(db_creation)

    def setup_engine(self, db_creation=None) -> None:
        """Setup engine and return engine if it already exists."""
        if self.engine:
            return
        self.engine = create_engine(db_creation, echo=False, pool_recycle=3600)
        self.Session.configure(bind=self.engine)

    def bootstrap(self) -> None:
        """Connects to the engine and creates the relevant tables."""
        connection = None
        error = Exception("Unable to connect to database with an unspecified error.")
        for i in range(2):
            try:
                connection = self.engine.connect()
            except Exception as error:
                logger.warning("MySQL server connection failed. Retrying...")
                time.sleep(i * 5)
                continue
        if not connection:
            raise error

        Base.metadata.create_all(self.engine)
        connection.close()


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(
        Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    customer_name = Column(String(45), nullable=False)
    customer_phone_number = Column(Integer(), nullable=False)

    customer_street = Column(String(45), nullable=True)
    customer_city = Column(String(45), nullable=True)
    customer_province = Column(String(45), nullable=True)
    customer_postal_code = Column(String(45), nullable=True)

    def convert_to_dict(self) -> dict:
        obj_dict = {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_phone_number": self.customer_phone_number,
            "customer_street": self.customer_street,
            "customer_city": self.customer_city,
            "customer_province": self.customer_province,
            "customer_postal_code": self.customer_postal_code,
        }
        return obj_dict


class Order(Base):
    __tablename__ = "order"
    order_id = Column(
        Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    order_date = Column(
        DateTime, default=datetime.now(timezone(offset=-timedelta(hours=4)))
    )
    order_payment_method = Column(String(45), nullable=False)
    order_type = Column(String(45), nullable=False)

    def convert_to_dict(self) -> dict:
        obj_dict = {
            "order_id": self.order_id,
            "date": self.date,
            "payment_method": self.payment_method,
            "order_type": self.order_type,
        }
        return obj_dict


class Food(Base):
    __tablename__ = "food"
    food_id = Column(
        Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    food_name = Column(String(45), nullable=False)
    food_category = Column(String(45), nullable=False)
    food_price = Column(Integer(), nullable=False)

    food_size = Column(String(45), nullable=True)

    def convert_to_dict(self) -> dict:
        obj_dict = {
            "food_id": self.food_id,
            "food_name": self.food_name,
            "food_category": self.food_category,
            "food_price": self.food_price,
            "food_size": self.food_size,
        }
        return obj_dict


class Addon(Base):
    __tablename__ = "addon"
    addon_id = Column(
        Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    addon_name = Column(String(45), nullable=False)
    addon_type = Column(String(45), nullable=False)
    addon_price = Column(Integer(), nullable=False)

    addon_size = Column(String(45), nullable=True)

    def convert_to_dict(self) -> dict:
        obj_dict = {
            "addon_id": self.addon_id,
            "addon_name": self.addon_name,
            "addon_type": self.addon_type,
            "addon_price": self.addon_price,
            "addon_size": self.addon_size,
        }
        return obj_dict


class CustomerOrder(Base):
    __tablename__ = "customer_order"
    customer_id = Column(
        Integer(), ForeignKey("customer.customer_id"), primary_key=True, nullable=False
    )
    order_id = Column(
        Integer(), ForeignKey("order.order_id"), primary_key=True, nullable=False
    )

    def convert_to_dict(self) -> dict:
        obj_dict = {"customer_id": self.customer_id, "order_id": self.order_id}
        return obj_dict


class OrderItem(Base):
    __tablename__ = "order_item"
    order_item_id = Column(
        Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    order_id = Column(Integer(), ForeignKey("order.order_id"), nullable=False)
    food_id = Column(Integer(), ForeignKey("food.food_id"), nullable=False)
    order_item_price = Column(Integer(), nullable=False)

    def convert_to_dictionary(self) -> dict:
        obj_dict = {
            "order_item_id": self.order_item_id,
            "order_id": self.order_id,
            "food_id": self.food_id,
            "order_item_price": self.order_item_price,
        }
        return obj_dict


class ItemMod(Base):
    __tablename__ = "item_mod"
    order_item_id = Column(
        Integer(),
        ForeignKey("order_item.order_item_id"),
        primary_key=True,
        nullable=False,
    )
    addon_id = Column(
        Integer(), ForeignKey("addon.addon_id"), primary_key=True, nullable=False
    )
    item_mod_qty = Column(Integer(), nullable=False)
    item_mod_price = Column(Integer(), nullable=False)

    def convert_to_dict(self) -> dict:
        obj_dict = {
            "order_item_id": self.order_item_id,
            "addon_id": self.addon_id,
            "item_mod_qty": self.item_mod_qty,
            "item_mod_price": self.item_mod_price,
        }
        return obj_dict


class ManageResturantData:
    """This manages the creation, modification, and removal of menu items, customers and orders."""

    def __init__(self) -> None:
        self.food_size_required = ["pizza"]

    def new_food_item(
        self,
        session: Session,
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
        session.add(food_details)
        session.commit()
        return food_details

    def update_food(self, session: Session, food_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given food item."""
        entity = session.query(Food).filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")

        required = [
            column.name for column in inspect(Food).c if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Food entity.\nThese are:\n{'\n'.join(required)}"
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

        update = (
            session.query(Food)
            .filter(Food.food_id == food_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def remove_food(self, session: Session, food_id: int) -> None:
        """Removes a food item from the menu."""
        entity = session.query(Food).filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_addon_item(
        self,
        session: Session,
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
        session.add(addon_details)
        session.commit()
        return addon_details

    def update_addon(self, session: Session, addon_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given addon."""
        entity = session.query(Addon).filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")

        required = [
            column.name
            for column in inspect(Addon).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Addon entity.\nThese are:\n{'\n'.join(required)}"
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

        update = (
            session.query(Addon)
            .filter(Addon.addon_id == addon_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def remove_addon(self, session: Session, addon_id: int) -> None:
        """Removes an addon item from the menu."""
        entity = session.query(Addon).filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_customer(
        self,
        session: Session,
        customer_name: str,
        customer_phone_number: int,
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
        session.add(customer_details)
        session.commit()
        return customer_details

    def update_customer(self, session: Session, customer_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given customer."""
        entity = (
            session.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
        if not entity:
            raise EntityNotFound("The customer does not exist in the database.")

        required = [
            column.name
            for column in inspect(Customer).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Customer entity.\nThese are:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Customer, req)] = kwargs.get(req)

        update = (
            session.query(Customer)
            .filter(Customer.customer_id == customer_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def remove_customer(self, session: Session, customer_id: int) -> None:
        """Removes a customer from the database."""
        entity = (
            session.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
        if not entity:
            raise EntityNotFound("The customer does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_order(
        self, session: Session, order_date, order_payment_method: str, order_type: str
    ) -> Order:
        """Adds order details to the database."""
        order_details = Order(
            order_date=order_date,
            order_payment_method=order_payment_method,
            order_type=order_type,
        )
        session.add(order_details)
        session.commit()
        return order_details

    def update_order(self, session: Session, order_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given order."""
        entity = session.query(Order).filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")

        required = [
            column.name
            for column in inspect(Order).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of Order entity.\nThese are:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(Order, req)] = kwargs.get(req)

        update = (
            session.query(Order)
            .filter(Order.order_id == order_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def remove_order(self, session: Session, order_id: int) -> None:
        """Removes an order from the database."""
        entity = session.query(Order).filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_customer_order(
        self, session: Session, customer_id: int, order_id: int
    ) -> CustomerOrder:
        """Adds customer order details to the database."""
        customer_order_details = CustomerOrder(
            customer_id=customer_id, order_id=order_id
        )
        session.add(customer_order_details)
        session.commit()
        return customer_order_details

    def remove_customer_order(
        self, session: Session, customer_id: int, order_id: int
    ) -> None:
        """Removes a customer order from the database."""
        entity = (
            session.query(CustomerOrder)
            .filter(CustomerOrder.customer_id == customer_id)
            .filter(CustomerOrder.order_id == order_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The customer order does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_order_item(
        self, session: Session, order_id: int, food_id: int, order_item_price: int
    ) -> OrderItem:
        """Adds order item details to the database."""
        order_item_details = OrderItem(
            order_id=order_id, food_id=food_id, order_item_price=order_item_price
        )
        session.add(order_item_details)
        session.commit()
        return order_item_details

    def update_order_item(self, session: Session, order_item_id: int, **kwargs) -> int:
        """Updates the value of an attribute of a given order item."""
        entity = (
            session.query(OrderItem)
            .filter(OrderItem.order_item_id == order_item_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")

        required = [
            column.name
            for column in inspect(OrderItem).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of OrderItem entity.\nThese are:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(OrderItem, req)] = kwargs.get(req)

        update = (
            session.query(OrderItem)
            .filter(OrderItem.order_item_id == order_item_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def find_all_order_items(self, session: Session, order_id: int) -> list:
        """Returns all order items for a given order."""
        entity = session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if not entity:
            raise EntityNotFound("The order does not have any items.")
        return [item.convert_to_dict() for item in entity]

    def remove_order_item(self, session: Session, order_item_id: int) -> None:
        """Removes an order item from the database."""
        entity = (
            session.query(OrderItem)
            .filter(OrderItem.order_item_id == order_item_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")
        session.delete(entity)
        session.commit()
        return

    def new_item_mod(
        self,
        session: Session,
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
        session.add(item_mod_details)
        session.commit()
        return item_mod_details

    def update_item_mod(
        self, session: Session, order_item_id: int, addon_id: int, **kwargs
    ) -> int:
        required = [
            column.name
            for column in inspect(ItemMod).c
            if not column.name.endswith("_id")
        ]
        if not any(i in kwargs for i in required):
            raise ValueError(
                f"Expected at least one attribute of ItemMod entity.\nThese are:\n{'\n'.join(required)}"
            )

        update_dict = {}

        for req in required:
            if kwargs.get(req):
                update_dict[getattr(ItemMod, req)] = kwargs.get(req)

        update = (
            session.query(ItemMod)
            .filter(ItemMod.order_item_id == order_item_id)
            .filter(ItemMod.addon_id == addon_id)
            .update(update_dict, synchronize_session=False)
        )
        session.commit()
        return update

    def remove_item_mod(
        self, session: Session, order_item_id: int, addon_id: int
    ) -> None:
        """Removes an item modification from the database."""
        entity = (
            session.query(ItemMod)
            .filter(ItemMod.order_item_id == order_item_id)
            .filter(ItemMod.addon_id == addon_id)
            .first()
        )
        if not entity:
            raise EntityNotFound(
                "The item modification does not exist in the database."
            )
        session.delete(entity)
        session.commit()
        return


class ViewResturantData:

    @staticmethod
    def view_food(session: Session, food_id: int) -> Query:
        """Returns the details of a given food item."""
        entity = session.query(Food).filter(Food.food_id == food_id).first()
        if not entity:
            raise EntityNotFound("The food item does not exist in the database.")
        return entity

    @staticmethod
    def view_addon(session: Session, addon_id: int) -> Query:
        """Returns the details of a given addon item."""
        entity = session.query(Addon).filter(Addon.addon_id == addon_id).first()
        if not entity:
            raise EntityNotFound("The addon item does not exist in the database.")
        return entity

    @staticmethod
    def view_customer(session: Session, customer_id: int) -> Query:
        """Returns the details of a given customer."""
        entity = (
            session.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
        if not entity:
            raise EntityNotFound(
                f'The customer "{customer_id}" does not exist in the database.'
            )
        return entity

    @staticmethod
    def view_customer_orders(session: Session, customer_id: int) -> list[Query]:
        """Returns all orders for a given customer."""
        entity = (
            session.query(CustomerOrder)
            .filter(CustomerOrder.customer_id == customer_id)
            .all()
        )
        if not entity:
            raise EntityNotFound("The customer does not have any orders.")
        return [item for item in entity]

    @staticmethod
    def view_order(session: Session, order_id: int) -> Query:
        """Returns the details of a given order."""
        entity = session.query(Order).filter(Order.order_id == order_id).first()
        if not entity:
            raise EntityNotFound("The order does not exist in the database.")
        return entity

    @staticmethod
    def view_order_grand_total(session: Session, order_id: int) -> int:
        """Returns the grand total of a given order."""
        order_entity = session.query(Order).filter(Order.order_id == order_id).first()

        if not order_entity:
            raise EntityNotFound("The order does not exist in the database.")

        order_items = (
            session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        )
        total = 0
        # XXX: This *might* be incredibly slow. I have no idea, I've literally never written SQL before.
        for item in order_items:
            total += int(item.order_item_price)
            mod = (
                session.query(ItemMod)
                .filter(ItemMod.order_item_id == item.order_item_id)
                .all()
            )
            for m in mod:
                total += int(m.item_mod_price)

        return total

    @staticmethod
    def view_order_customer(session, order_id) -> Query:
        """Returns the customer details for a given order."""
        entity = (
            session.query(CustomerOrder)
            .filter(CustomerOrder.order_id == order_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The order does not have a customer.")
        return entity

    @staticmethod
    def view_order_item(session: Session, order_item_id: int) -> Query:
        """Returns the details of a given order item."""
        entity = (
            session.query(OrderItem)
            .filter(OrderItem.order_item_id == order_item_id)
            .first()
        )
        if not entity:
            raise EntityNotFound("The order item does not exist in the database.")
        return entity

    @staticmethod
    def view_order_items(session: Session, order_id: int) -> list[Query]:
        """Returns the items in a given order."""
        order_items = (
            session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        )
        if not order_items:
            raise EntityNotFound("The order does not have any items.")
        return [item for item in order_items]

    @staticmethod
    def view_item_mods(session: Session, order_item_id: int) -> list[Query]:
        """Returns all item modifications for a given order item."""
        entity = (
            session.query(ItemMod).filter(ItemMod.order_item_id == order_item_id).all()
        )
        if not entity:
            raise EntityNotFound("The order item does not have any modifications.")
        return [item for item in entity]

from datetime import datetime, timedelta, timezone

from .. import db

Column = db.Column
String = db.String
Integer = db.Integer
DateTime = db.DateTime
ForeignKey = db.ForeignKey

Base = db.Model


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

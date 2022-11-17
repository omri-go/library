from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class mydatabase():

    def test(self): return "testt"

    def __init__(self):
        # Create the database
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        # fill out the catalog
        self.createCatalog()

        # create test customers
        c1 = Customer("itay")
        c2 = Customer("maya")

        # # create an order
        order = self.createOrder(c1.customer_name, [Item(
            "Tank", 1222226.50), Item("Submarine", 18.09)])
        order = self.createOrder(c1.customer_name, [Item(
            "popcorn", 6.50), Item("Submarine", 13.09)])
        order = self.createOrder(c2.customer_name, [self.session.query(Item)[
                                 1], self.session.query(Item)[0]])

        self.displayTheCatalog()
        # display items from a customer/order
        self.displayOrderItems("maya")
        self.displayOrderItems("itay")
        self.displayOrderItems(order_id=1)
        self.displayOrderItems(order_id=2)

    # create a catalog
    def createCatalog(self):
        tshirt, mug, hat, crowbar = (
            Item("SA T-Shirt", 10.99),
            Item("SA Mug", 6.50),
            Item("SA Hat", 8.99),
            Item("MySQL Crowbar", 16.99),
        )
        self.session.add_all([tshirt, mug, hat, crowbar])
        self.session.commit()

    def createOrder(self, customerName, items=[]):
        # create an order
        o = Order(customerName)
        for item in items:
            o.order_items.append(OrderItem(item))
        self.session.add(o)
        return o

    def displayOrderItems(self, customer_name="", order_id=-1):
        # query the order, print items
        if customer_name:
            for order in self.session.query(Order).filter_by(customer_name=customer_name).all():
                print(
                    [
                        (order_item.item.description,
                         order_item.price, order_item.order_id)
                        for order_item in order.order_items
                    ]
                )
        if order_id > -1:
            for order in self.session.query(Order).filter_by(order_id=order_id).all():
                print(
                    [
                        (order_item.item.description,
                         order_item.price, order_item.order_id)
                        for order_item in order.order_items
                    ]
                )
        # display a catalog

    def displayTheCatalog(self):
        catalog = self.session.query(Item).all()
        # print(len(catalog))
        for item in catalog:
            print(item)


# ############# end class

# Tables


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order = relationship('Order', uselist=True, backref=backref('Customer'))

    def __init__(self, customer_name):
        self.customer_name = customer_name


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now())
    order_items = relationship(
        "OrderItem", cascade="all, delete-orphan", backref="order"
    )

    def __init__(self, customer_name):
        self.customer_name = customer_name

    customer_id = Column(Integer, ForeignKey('customers.id'))


class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    description = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, description, price):
        self.description = description
        self.price = price

    def __repr__(self):
        return "Item(%r, %r,%r)" % (self.description, self.price, self.item_id)


class OrderItem(Base):
    __tablename__ = "orderitem"
    order_id = Column(Integer, ForeignKey("order.order_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    price = Column(Float, nullable=False)

    def __init__(self, item, price=None):
        self.item = item
        self.price = price or item.price

    item = relationship(Item, lazy="joined")

# actions


# if __name__ == "__main__":
#     engine = create_engine("sqlite://")
#     Base.metadata.create_all(engine)

#     session = Session(engine)

    # createCatalog()
    # # create customers
    # c1 =Customer("itay")
    # c2 =Customer("maya")

    # # create an order
    # order = createOrder(c1.customer_name,[Item("Tank", 1222226.50),Item("Submarine", 18.09)])
    # order = createOrder(c1.customer_name,[Item("popcorn", 6.50),Item("Submarine", 13.09)])
    # order = createOrder(c2.customer_name,[session.query(Item)[1],session.query(Item)[0]])

    # # update a product price in order number 0
    # order.order_items[0].price=5555

    # session.commit()

    # # display all our products
    # print("Our Products")
    # displayTheCatalog()

    # # display items from a customer order
    # displayOrderItems("maya")
    # displayOrderItems("itay")
    # displayOrderItems(order_id=1)
    # displayOrderItems(order_id=2)

from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum

Customer = namedtuple('Customer', 'name fidelity')

class Promotion(Enum):
    FidelityPromo = 1
    BulkItemPromo = 2
    LargeOrderPromo = 3

class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # Context

    def __init__(self, customer, cart, promotion):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
        self.__total = 0.0

    def total(self):
        self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        discount = 0
        if self.promotion == Promotion.FidelityPromo:
            discount = self.total() * 0.05 if self.customer.fidelity >= 1000 else 0
        elif self.promotion == Promotion.BulkItemPromo:
            for item in self.cart:
                if item.quantity >= 20:
                    discount += item.total() * 0.1
        elif self.promotion == Promotion.LargeOrderPromo:
            distinct_items = {item.product for item in self.cart}
            if len(distinct_items) >= 10:
                discount = self.total() * 0.07

        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
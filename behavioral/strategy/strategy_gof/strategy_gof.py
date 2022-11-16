from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
from dataclasses import dataclass
from typing import Optional

Customer = namedtuple('Customer', 'name fidelity')


class Promotion(Enum):
    FidelityPromo = 1
    BulkItemPromo = 2
    LargeOrderPromo = 3


class DiscountStrategy(ABC):
    promotions = {}

    @classmethod
    def register_promotion(cls, id: Promotion):
        def deco(deco_cls):
            cls.promotions[id] = deco_cls()
            return deco_cls
        return deco

    @abstractmethod
    def get_discount(self, order: "Order"):
        pass


class NullPromo(DiscountStrategy):
    """No discount at all"""

    def get_discount(self, order: "Order") -> float:
        return 0


@DiscountStrategy.register_promotion(Promotion.FidelityPromo)
class FidelityPromo(DiscountStrategy):
    def get_discount(self, order: "Order"):
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


@DiscountStrategy.register_promotion(Promotion.LargeOrderPromo)
class LargeOrderPromo(DiscountStrategy):
    def get_discount(self, order: "Order"):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0


@DiscountStrategy.register_promotion(Promotion.BulkItemPromo)
class BulkItemPromo(DiscountStrategy):
    def get_discount(self, order: "Order"):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount


class PromotionGroup(DiscountStrategy):
    """Composite pattern for DiscountStrategies"""
    def __init__(self):
        self._promotions = []

    def add_promo(self, promotion: DiscountStrategy):
        self._promotions.append(promotion)

    def get_discount(self, order: "Order"):
        return max((promo.get_discount(order) for promo in self._promotions), default=0)

class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # Context

    def __init__(self, customer, cart, promotion: Optional[Promotion]):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = DiscountStrategy.promotions.get(
            promotion, NullPromo())
        self.__total = 0.0

    def total(self):
        self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        return self.total() - self.promotion.get_discount(self)

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class OrderAlt:  # Context

    def __init__(self, customer, cart, promotion: DiscountStrategy):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion or NullPromo()
        self.__total = 0.0

    def total(self):
        self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        return self.total() - self.promotion.get_discount(self)

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


if __name__ == "__main__":
    print(DiscountStrategy.promotions)

    john = Customer('John Doe', 0)
    large_cart = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]

    black_friday = PromotionGroup()
    black_friday.add_promo(FidelityPromo())
    black_friday.add_promo(LargeOrderPromo())
    black_friday.add_promo(BulkItemPromo())

    order = OrderAlt(john, large_cart, black_friday)
    print(f"Order: {order.total()=}, {order.due()=}")

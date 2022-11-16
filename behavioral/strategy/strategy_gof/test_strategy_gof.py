from strategy_gof import *
import pytest


class TestFidelityPromo:
    def test_when_no_fidelity_points_no_discount_applied(self):
        cart = [LineItem('banana', 4, .5), LineItem(
            'apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]

        john = Customer('John Doe', 0)
        order = Order(john, cart, Promotion.FidelityPromo)
        assert order.total() == 42
        assert order.total() == order.due()

    def test_when_fidelity_points_over_1000_discount_applied(self):
        cart = [LineItem('banana', 4, .5), LineItem(
            'apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]

        john = Customer('John Doe', 1100)
        order = Order(john, cart, Promotion.FidelityPromo)
        assert order.total() == 42
        assert order.due() == 39.90


@pytest.fixture
def bulk_cart():
    return [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]


def test_bulk_purchase_(bulk_cart):
    john = Customer('John Doe', 0)
    order = Order(john, bulk_cart, Promotion.BulkItemPromo)
    assert order.total() == 30
    assert order.due() == 28.50


@pytest.fixture
def large_cart():
    return [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]


def test_long_purchase(large_cart):
    john = Customer('John Doe', 0)
    order = Order(john, large_cart, Promotion.LargeOrderPromo)
    assert order.total() == 10
    assert order.due() == 9.30

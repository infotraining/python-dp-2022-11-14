import abc


class Coffee(abc.ABC):
    @abc.abstractproperty
    def price(self) -> float:  # type:ignore
        """returns price of coffee"""

    @abc.abstractproperty
    def description(self) -> str:  # type:ignore
        """returns description of coffee"""

    @abc.abstractmethod
    def prepare(self) -> None:
        """prepares a coffee"""


class BaseCoffee(Coffee):
    def __init__(self, price, description):
        self.__price = price
        self.__description = description

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description


class Espresso(BaseCoffee):
    def __init__(self, price=4.0):
        super().__init__(price, "Espresso")

    def prepare(self):
        print("Making a perfect espresso: 8g of coffee, 96 Celsius, 16 bar")


class Cappuccino(BaseCoffee):
    def __init__(self, price=6.0):
        super().__init__(price, "Cappuccino")

    def prepare(self):
        print("Making an espresso combined with a perfect milk foam")


class Latte(BaseCoffee):
    def __init__(self, price=9.0):
        super().__init__(price, "Latte")

    def prepare(self):
        print("Making a perfect latte")

#######################################
# Decorators
######################################
# Prices of condiments:
#  - Whipped Cream: 2.5
#  - Whisky: 10.0
#  - ExtraEspresso: 4.0
######################################

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee, price, description):
        self.__coffee = coffee
        self.__price = price
        self.__description = description

    @property
    def price(self):
        return self.__price + self.__coffee.price

    @property
    def description(self):
        return f"{self.__coffee.description} + {self.__description}"

    def prepare(self) -> None:
        return self.__coffee.prepare()


class Whipped(CoffeeDecorator):
    def __init__(self, component: Coffee, price=2.5, description="Whipped Cream"):
        super().__init__(component, price, description)

    def prepare(self):
        super().prepare()
        print("Adding a whipped cream")


class Whisky(CoffeeDecorator):
    def __init__(self, component: Coffee, price=10.0, description="Whisky"):
        super().__init__(component, price, description)

    def prepare(self):
        super().prepare()
        print("Pouring a 50cl of whisky")


class ExtraEspresso(CoffeeDecorator):
    def __init__(self, component: Coffee, price=4.0, description="Extra Espresso"):
        super().__init__(component, price, description)

    def prepare(self):
        super().prepare()
        Espresso().prepare()


class CoffeeBuilder:
    def __init__(self):
        self.__coffee = None

    def create_base(self, base):
        if not issubclass(base, BaseCoffee):
            raise TypeError("base must be derived from BaseCoffee")

        self.__coffee = base()
        return self

    def add(self, *condiments):
        
        assert self.__coffee

        for condiment in condiments:
            if not issubclass(condiment, CoffeeDecorator):
                raise TypeError("the condiment must be derived from Derived")

            self.__coffee = condiment(self.__coffee)

        return self

    def get_coffee(self):
        return self.__coffee


if __name__ == "__main__":

    coffee = Whisky(ExtraEspresso(Cappuccino()))
    print(f"Price: {coffee.price}$")
    print(f"Description: {coffee.description}")
    coffee.prepare()

    print('-' * 60)

    coffee = Whisky(Whisky(Whipped(Whisky(Espresso()))))
    print(f"Price: {coffee.price}$")
    print(f"Description: {coffee.description}")
    coffee.prepare()

    print('-' * 60)

    coffee = CoffeeBuilder() \
        .create_base(Espresso) \
        .add(Whisky, ExtraEspresso) \
        .add(Whipped) \
        .get_coffee()

    print(f"Price: {coffee.price}$")
    print(f"Description: {coffee.description}")
    coffee.prepare()



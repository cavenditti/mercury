from datetime import datetime, timedelta

from .Product import Product
from .common import HollowType

class PositionType(metaclass=HollowType):
    pass

class PositionMetaclass(type):
    def short(cls, product: Product, instant: datetime, quantity: int):
        return Position(product, instant, quantity, Position.Short)
    def long(cls, product: Product, instant: datetime, quantity: int):
        return Position(product, instant, quantity, Position.Long)
    def none(cls, product: Product, instant: datetime, quantity: int):
        return Position(product, instant, quantity, Position.Closed)

class Position(metaclass=PositionMetaclass):
    """Position.
    Possible types of position:
    - Closed
    - Short
    - Long
    """

    class Short(PositionType):
        pass

    class Long(PositionType):
        pass

    class Closed(PositionType):
        pass

    def __init__(self, product: Product, instant: datetime, quantity: int, positionType: PositionType):
        self.type          = positionType
        self.opening_time  = instant
        self.quantity      = quantity
        self.inital_price  = 0 #FIXME Product.at(instant)
        self.current_price = self.inital_price

    @property
    def is_open(self):
        return self.type != Position.none

    @property
    def is_short(self):
        return self.type == Position.short

    @property
    def is_long(self):
        return self.type == Position.long

    def update_price(self, new_price: float):
        self.current_price = new_price

    def duration(self, now: datetime) -> timedelta:
        return timedelta(now - self.start)

    @property
    def value(self) -> float:
        return (self.inital_price + self.gains()) * quantity

    @property
    def gains(self) -> float:
        if self.type == Position.long:
            return self.current_value - self.inital_value
        elif self.type == Position.short:
            return self.inital_value - self.current_value
        else:
            return 0

    def __str__(self) -> str:
        return "Position('{}',{}, at {})".format(self.type, self.quantity, self.opening_time)

    def __repr__(self) -> str:
        return self.__str__()


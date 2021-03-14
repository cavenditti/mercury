from datetime import datetime, timedelta
import copy

from .Product import Product
from .common import HollowType

class PositionType(metaclass=HollowType):
    pass

class PositionMetaclass(type):
    def short(cls, product: Product, instant: datetime, quantity: int):
        return Position(product, instant, quantity, Position.Short)
    def long(cls, product: Product, instant: datetime, quantity: int):
        return Position(product, instant, quantity, Position.Long)
    def closed(cls, product: Product, instant: datetime):
        return Position(product, instant, 0, Position.Closed)

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
        if quantity == 0:
            positionType = Position.Closed
        self.product       = product
        self.type          = positionType
        self.opening_time  = instant
        self.quantity      = quantity
        self.inital_price  = round(product.close[instant], 5)
        self.current_price = self.inital_price

    def copy(self):
        return Position(self.product, copy.deepcopy(self.opening_time), copy.deepcopy(self.quantity), copy.deepcopy(self.type))

    @property
    def is_open(self):
        return self.type != Position.Closed

    @property
    def is_short(self):
        return self.type == Position.Short

    @property
    def is_long(self):
        return self.type == Position.Long

    def update_price(self, new_price: float):
        self.current_price = round(new_price, 5)

    def duration(self, now: datetime) -> timedelta:
        return timedelta(now - self.start)

    @property
    def value(self) -> float:
        return round(self.current_price * self.quantity, 2)

    @property
    def gains(self) -> float:
        if self.type == Position.Long:
            return self.value - self.inital_value
        elif self.type == Position.Short:
            return self.inital_value - self.value
        else:
            return 0.

    def __str__(self) -> str:
        return "Position('{}',{}, at {})".format(self.type, self.quantity, self.opening_time)

    def __repr__(self) -> str:
        return self.__str__()


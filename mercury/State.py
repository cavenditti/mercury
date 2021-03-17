from collections.abc import Sequence,Mapping
import copy

from .Product  import Product
from .Position import Position
from .Signal   import Signal

class State(Mapping[Product,(Position, Signal)]):
    """State."""

    def __init__(self, source=None, cash : float = 0):
        """__init__.

        :param source:
        """

        if type(source) == State:
            self.map = copy.deepcopy(source.map)
            self.product_map = source.product_map
            self.cash = copy.deepcopy(source.cash)
            # Don't take old signals
            #FIXME
            for p in self:
                self.update_signal(p, Signal.keep())
        else:
            self.map = {}
            self.product_map = {}
            self.cash = cash
            if source is None:
                return
            elif isinstance(source, Sequence) and isinstance(source[0], Product):
                for product in source:
                    self.map[product.ISIN] = (Position.closed(product, product.index[0]),Signal())
                    self.product_map[product.ISIN] = product
            else:
                raise TypeError('State can only be created from a state or a list of products')

    def __getitem__(self, product: Product) -> (Position, Signal):
        return self.map.__getitem__(product)

    def __iter__(self):
        for isin in self.map:
            try:
                yield self.product_map[isin]
            except:
                pass

    def __len__(self):
        return self.map.__len__()

    def new(self):
        return State(self)

    def update(self, product: Product, position: Position, signal: Signal) -> bool:
        """update.

        :param product:
        :type product: Product
        :param position:
        :type position: Position
        :param signal:
        :type signal: Signal
        """

        if self.enough_cash(position):
            return False

        # If we're opening or closing a position the readly available cash changes
        if signal.type != Signal.Keep and position is not None:
            self.cash = round(self.cash + self.map[product.ISIN][0].value - position.value, 2)
        self.map[product.ISIN] = (position, signal)

        return True

    def update_position(self, product : Product, position : Position):
        return self.update(product, position, self.signal(product))

    def update_signal(self, product : Product, signal : Signal):
        return self.update(product, self.position(product), signal)

    def enough_cash(self, position : Position):
        return position.value > self.cash

    def positions(self, position_type):
        return [isin for isin in self.map.keys() if self.map[isin][0].type() == position_type]

    def position(self, product):
        return self.map[product.ISIN][0]

    def signal(self, product):
        return self.map[product.ISIN][1]

    @property
    def total_value(self) -> float:
        """total_value.

        :returns: Total value of available cash and open positions
        :rtype: float
        """
        total_value = self.cash
        for position,signal in self.map.values():
            total_value += position.value
        return round(total_value, 2)

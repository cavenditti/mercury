from collections.abc import Sequence,Mapping

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
            # Don't take old signals
            self.map = {}.fromkey(source.map, (source.map.items()[0], None))
            self.cash = source.cash

        self.map = {}
        self.cash = cash
        if source is None:
            return
        elif isinstance(source, Sequence) and isinstance(source[0], Product):
            for product in source:
                self.map[product.ISIN] = (None,Signal())
        else:
            raise TypeError('State can only be created from a state or a list of products')

    def __getitem__(self, product: Product) -> (Position, Signal):
        return self.map.__getitem__(product)

    def __iter__(self):
        return self.map.__iter__()

    def __len__(self):
        return self.map.__len__()

    def update(self, product: Product, position: Position, signal: Signal) -> bool:
        """update.

        :param product:
        :type product: Product
        :param position:
        :type position: Position
        :param signal:
        :type signal: Signal
        :rtype: bool
        """

        # If we're opening or closing a position the readly available cash changes
        if signal.type != Signal.keep and position is not None:
            self.cash = self.cash + self.map[product.ISIN][0].value - position.value

        self.map[product.ISIN] = (position, signal)

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
            try:
                total_value += position.value
            except AttributeError:
                pass
        return total_value

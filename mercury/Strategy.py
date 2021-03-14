from collections.abc import Mapping, Sequence
from datetime import datetime

from .State    import State
from .Product  import Product
from .Position import Position
from .Signal   import Signal
from .Results  import Results

class Strategy:
    """Strategy."""

    def __init__(self, *args, **kwargs):
        """__init__.
        Strategies should pass all the required parameters to the constructor without overloading it
        (unless necessary for whatever reason, of course).

        All global parameters are kept in the object __dict__. Product-specific parameters
        should be kept directly in the Product objects

        :param args:
        :param kwargs:
        """

        for ak,av in kwargs.items():
            self.__dict__[ak] = av


    def train(self, product_slices: Sequence[Product]) -> Sequence[Product]:
        """train function.
        Takes a sequence of products and returns a sequence of product to which the strategy is applicable

        :param product_slices:
        :type product_slices: Sequence[Product]
        :rtype: Sequence[Product]
        """
        return product_slices

    def play(self, position: Position, product_slice: Product) -> Signal:
        """play.
        Runs the strategy on a specific day for a specific product

        :param position:
        :type position: Position
        :param product_slice:
        :type product_slice: Product
        :rtype: Signal
        """
        raise NotImplementedError("Strategy classes must implement a play function")

    def planner(self, state: State, date : datetime) -> State:
        """planner.

        :param state:
        :type state: Mapping[Product,(Position,Signal)]
        :rtype: Mapping[Product, Signal]
        """
        raise NotImplementedError("Strategy classes must implement a planner function")

    def metrics(self, results : Results) -> Results:
        """metrics.
        TODO

        results['metric_name'] = 'Metric Pretty Name', metric_value

        :param results:
        :type results: Results
        :rtype: Results
        """
        return results


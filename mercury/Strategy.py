from collections.abc import Mapping, Sequence

from . import Product,Position,Signal

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

    def planner(self, state: Mapping[Product,(Position,Signal)]) -> Mapping[Product, Signal]:
        """planner.

        :param state:
        :type state: Mapping[Product,(Position,Signal)]
        :rtype: Mapping[Product, Signal]
        """
        raise NotImplementedError("Strategy classes must implement a planner function")

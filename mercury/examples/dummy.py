#!/usr/bin/env python
if __name__ == "__main__" and __package__ is None:
    __package__ = "mercury.examples"

from mercury import Strategy
from mercury import Signal

class dummy_strategy(Strategy):
    def __init__(self):
        pass

    def play(self, position, product_slice):
        return Signal.keep()

    def planner(self, state, date):
        return state

if __name__ == "__main__":
    print("Dummy strategy example")
    from mercury import Trader
    dummy = dummy_strategy()
    trader = Trader(dummy)
    trader.import_data('test_data/finaldestination2k.csv')
    trader.run()

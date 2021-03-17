#!/usr/bin/env python
if __name__ == "__main__" and __package__ is None:
    __package__ = "mercury.examples"

from mercury import *

class SMA(Strategy):
    def __init__(self, periods=3):
        self.periods = periods

    def play(self, position, product_slice):
        # Calcultate SMA (only first time)
        # TODO automatically keep a cache in Product
        #print(len(product_slice))

        sma = product_slice.SMA(timeperiod=self.periods)

        current_date = product_slice.index[-1]
        current_price = product_slice.close.iloc[-1]
        last_sma = sma[current_date]

        if position.is_open:
            if ((position.is_short and current_price > sma[current_date]) or
                    (position.is_long and current_price < sma[current_date])):
                #print('close {} on {}'.format(position.type, product_slice.ISIN))
                return Signal.close()
        else:
            if product_slice.crossed_up(last_sma):
                #print('open long on {}'.format(product_slice.ISIN))
                return Signal.long()
            elif product_slice.crossed_down(last_sma):
                #print('open short on {}'.format(product_slice.ISIN))
                return Signal.short()

        return Signal.keep()

    def planner(self, state, date):
        n = 0
        for p in state:
            sig_type = state.signal(p).type
            if sig_type == Signal.Open_long or sig_type == Signal.Open_short:
                n+=1
        pos_value = 0
        if n != 0:
            pos_value = state.cash / 2 * n
            if pos_value == float('-inf') or pos_value == float('inf'):
                return state
        for p in state:
            sig_type = state.signal(p).type
            if sig_type == Signal.Open_long:
                try:
                    quantity = round(pos_value / p.close.loc[date])
                except Exception as e:
                    print('Ahia', p.ISIN, e.__class__.__name__, e)
                    print(f'pos_value: {pos_value}')
                    print(f'p.close.loc[date]: {p.close.loc[date]}')
                    quantity = 0
                state.update_position(p, Position.long(p, date, quantity))
            elif sig_type == Signal.Open_short:
                try:
                    quantity = round(pos_value / p.close.loc[date])
                except Exception as e:
                    print('Ahia', p.ISIN, e.__class__.__name__, e)
                    quantity = 0
                state.update_position(p, Position.short(p, date, quantity))
            elif sig_type == Signal.Close:
                state.update_position(p, Position.closed(p, date))
        return state

if __name__ == "__main__":
    print("SMA strategy example")
    from mercury import Trader
    sma_strategy = SMA()
    trader = Trader(sma_strategy)
    trader.import_data('../../data/synthetic/sintetici2k.csv')
    trader.run()
    trader.print_results()

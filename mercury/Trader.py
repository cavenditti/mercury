# This will become the default behaviour starting from Python 3.10
from __future__ import annotations

from collections.abc import Sequence
import pandas as pd

from .Product  import Product
from .Strategy import Strategy
from .Position import Position
from .Signal   import Signal
from .State    import State
from .Results  import Results
from .common   import time_interval

#TODO move into Product
#TODO ensure the index is the same for all products (make this a DataFrame?)
class Data(list):
    def slice(self, ti: time_interval) -> Data:
        new_list = Data()
        for a in self:
            new_list.append(a.slice(ti))
        return new_list

    @property
    def dindex(self):
        return self[0].index

    @property
    def dsize(self):
        return self[0].index.size

    @property
    def ISINs(self):
        return [x.ISIN for x in self]

#TODO replace all Sequence[Product]
class Trader:
    """Trader."""

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    @staticmethod
    def __test_slicer(train_slices: Sequence[Product], data, test_interval) -> Sequence[Product]:
        """__test_slicer.
        Takes the slices from trainings and gets corresponding slices for test from data

        :param train_slices:
        :type train_slices: Sequence[Product]
        :param test_interval:
        :rtype: Sequence[Product]
        """
        return Data([p.slice(test_interval) for p in data if p.ISIN in train_slices.ISINs])

    def __check_valid_transition(old_state : State, new_state : State) -> bool:
        """__check_valid_transition.
        Checks if the strategy has created a new invalid state (e.g. opening more positions the
        available cash would have allowed)

        :param old_state:
        :type old_state: State
        :param new_state:
        :type new_state: State
        :rtype: bool
        """

        #return round(old_state.total_cash + ) == round(new_state.total_cash)
        # FIXME not implemented
        return True

    def __tradesim(self, product_slices: Sequence[Product], trade_interval: time_interval,
                     cash : float) -> Sequence[State]:
        """__tradesim.
        Run trading simulation during across given product slices

        :param product_slices:
        :type product_slices: Sequence[Product]
        :param trade_interval:
        :type trade_interval: time_interval
        :rtype: Sequence[State]
        """

        product_slices = product_slices.slice(time_interval)
        # Create states for each day
        state_sequence = [State(product_slices, cash)]*product_slices.dsize

        '''
        It goes like this:

        for day in interval:
            for product in product_slices:
                self.strategy.play()
            self.strategy.planner()
        '''
        # We use int indeces from index so we easly get prevoius and next when needed
        for i in range(product_slices.dsize-1):
            for product in product_slices:
                position = state_sequence[i].position(product)
                signal = self.strategy.play(position,product)

                state_sequence[i].update(product, position, signal)

            state_sequence[i+1] = self.strategy.planner(state_sequence[i])

        return state_sequence

    # Is it better called an "interval" or a "range"?

    def run(self, test_interval : time_interval = None, train_interval : time_interval = None, cash : float = 10000):
        # train on given interval (if None just does it on the whole data)
        # then test on given interval (if None just does it on the whole data)
        # TODO it would be better to train on all the data available before the test period if no train_interval is passed
        self.__train_slices = self.strategy.train(self.data.slice(train_interval))
        self.train_results = self.__tradesim(self.__train_slices, train_interval, cash)

        self.__testing_set = self.__test_slicer(self.__train_slices, self.data, test_interval)

        self.test_results = self.__tradesim(self.__testing_set, test_interval, cash)

        self.results = Results(self.train_results, self.test_results)
        s_results = self.strategy.metrics(self.results)

    def print_results(self):
        print(self.results)


    def load_data(self, path: str):
        """load_data.

        :param dir:
        :type dir: str
        """
        #self.data = data?
        raise NotImplementedError

    def import_data(self, path: str):
        """import_data.
        import old data from CSVs with only closing prices

        :param path:
        :type path: str
        """

        df = pd.read_csv(path, index_col='date')
        self.data = Data()
        for column in df.columns:
            df[column].name = 'Close'
            self.data.append(Product(column, 'stock', data={'Close' : df[column]}))



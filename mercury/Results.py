from collections.abc import Sequence
from . import Product, State

class Results:
    def __init__(self, train_results : Sequence[State], test_results : Sequence[State]):
        value = [x.total_value for x in test_results]
        self.__dict__['value'] = None, value
        self.__dict__['starting_value'] = 'Starting value:', value[0]
        self.__dict__['final_value'] = 'Final value:', value[-1]
        self.__dict__['p_l'] = 'P&L:', (value[-1]/value[0]-1)*100, '%'
        self.__dict__['dd'] = 'Maximum Drawdown:', self.calculate_dd(value)

    def calculate_dd(self, values):
        max_value = values[0]
        max_dd=0
        i=0
        for value in values:
            if value >= max_value:
                max_value = value
                i = 0
                continue
            i+=1
            if i > max_dd:
                max_dd = i
        return max_dd

    def __str__(self) -> str:
        ret_str = ''
        for metric in self.__dict__:
            if self.__dict__[metric][0] is None:
                continue
            for s in self.__dict__[metric]:
                ret_str += str(s) + ' '
            ret_str += '\n'
        return ret_str

    def __repr__(self) -> str:
        return self.__str__()


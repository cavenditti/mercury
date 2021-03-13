from .common import HollowType

class SignalType(metaclass=HollowType):
    pass

class SignalMetaclass(type):
    def short(cls, strength : int = 0):
        return Signal(Signal.Open_short, strength)
    def long(cls, strength : int = 0):
        return Signal(Signal.Open_long, strength)
    def close(cls, strength : int = 0):
        return Signal(Signal.Close, strength)
    def keep(cls, strength : int = 0):
        return Signal(Signal.Keep, strength)

class Signal(metaclass=SignalMetaclass):
    """Signal.
    Possible types of signals:
    - Keep (do nothing)
    - Open long
    - Open short
    - Close position

    """

    class Open_short(SignalType):
        pass

    class Open_long(SignalType):
        pass

    class Close(SignalType):
        pass

    class Keep(SignalType):
        pass

    def __init__(self, signalType = Keep, strength : int = 0):
        """__init__.

        :param signalType:
        :param strength:
        :type strength: int
        """

        # Only accepts classes that inherit from SignalType
        if not issubclass(signalType, SignalType):
            raise TypeError('Invalid position type')
        self.type = signalType
        self.strength = strength

    def __str__(self) -> str:
        return str(self.type)

    def __repr__(self) -> str:
        return "Signal('{}',{})".format(self.type, self.strength)


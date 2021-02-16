from .common import HollowType

class SignalType(metaclass=HollowType):
    pass

class Open_short(SignalType):
    pass

class Open_long(SignalType):
    pass

class Close(SignalType):
    pass

class Keep(SignalType):
    pass

class SignalMetaclass(type):
    @property
    def short(cls):
        return Open_short
    @property
    def long(cls):
        return Open_long
    @property
    def close(cls):
        return Close
    @property
    def keep(cls):
        return Keep

class Signal(metaclass=SignalMetaclass):
    """Signal.
    Possible types of signals:
    - Keep (do nothing)
    - Open long
    - Open short
    - Close position

    """

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


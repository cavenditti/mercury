class HollowType(type):
    def __call__(cls, *a, **kw):
        raise TypeError('This class cannot be instantiated.')
    def __str__(self):
        return self.__name__.replace('_', ' ')
    def __repr__(self):
        return "<{}: '{}'>".format(self.__base__,str(self))


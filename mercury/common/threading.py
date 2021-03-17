from threading import Lock

t_print_lock = Lock()
def t_print(*a, **b):
    """Thread safe print function"""
    with t_print_lock:
        print(*a, **b)

class T_Counter:
    """ Thread-safe counter.
    TODO make this into a wrapper around pool.map() to do everything by itself
    """
    __instance__ = None

    def __init__(self, message, end):
        if type(end) is not int:
            raise TypeError('end should be \'int\', not {}'.format(type(end)))

        self.message = message
        self.end = end
        self.i = 0
        self.start_time = time.perf_counter()
        with t_print_lock:
            T_Counter.__instance__ = self
            sys.stdout.write("\r"+'{}: 0/{}'.format(self.message, self.end))
            sys.stdout.flush()

    @staticmethod
    def tick(name=None):
        """ Static method to update the counter.
        """
        with t_print_lock:
            if name is None:
                T_Counter.__instance__.i = T_Counter.__instance__.i + 1
                sys.stdout.write("\r"+'{}: {}/{}'.format(T_Counter.__instance__.message,
                    T_Counter.__instance__.i, T_Counter.__instance__.end))
                sys.stdout.flush()
            else:
                T_Counter.__instance__.i = T_Counter.__instance__.i + 1
                sys.stdout.write("\r"+'{}: {}/{}{:>50}'.format(T_Counter.__instance__.message,
                    T_Counter.__instance__.i, T_Counter.__instance__.end, T_Counter.__instance__.message))
                sys.stdout.flush()

    @staticmethod
    def done():
        with t_print_lock:
            elapsed = time.perf_counter() - T_Counter.__instance__.start_time
            sys.stdout.write("\r"+'{}: Done in {}s\n'.format(T_Counter.__instance__.message, elapsed))
            sys.stdout.flush()
            T_Counter.__instance__ = None

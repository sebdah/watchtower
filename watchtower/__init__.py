""" Init file for Watchtower """
import time


SERVICES = []


class Service:
    """ Definition of a Service """
    name = None
    monitors = {}

    def __init__(self, name):
        """ Constructor

        :type name: str
        :param name: Service name
        :returns: None
        """
        self.name = name

    def add(self, name, monitor, interval=300, args=[], kwargs={}):
        """ Add a monitor to the monitoring list

        :type name: str
        :param name: Name of the monitor
        :type monitor: function
        :param monitor: A Python function to execute
        :type interval: int
        :param interval: How many seconds to sleep between each check
        :type args: list
        :param args: List of positional arguments to use
        :type kwargs: dict
        :param kwargs: Dictionary with keyword arguments
        :returns: None
        """
        self.monitors[name] = {
            'monitor': monitor,
            'interval': int(interval),
            'args': args,
            'kwargs': kwargs
        }

        self.log(
            'Added monitor "{monitor_name}" with interval {interval}'.format(
                monitor_name=name,
                interval=interval),
            level='DEBUG')

    def execute(self, name):
        """ Execute the given monitor

        :type name: str
        :param name: Name of the monitor
        :returns: Result of monitor function or None
        """
        try:
            # Do not do anything unless the interval is right
            if int(time.time()) % self.monitors[name]['interval'] != 0:
                return None

            return self.monitors[name]['monitor'](
                *self.monitors[name]['args'],
                **self.monitors[name]['kwargs'])
        except KeyError:
            return None

    def execute_all(self):
        """ Execute all monitors

        :returns: dict -- {'monitor': return_value}
        """
        results = {}

        for monitor in self.monitors:
            result = self.execute(monitor)
            if result:
                results[monitor] = result

        return results

    def log(self, message, level='INFO'):
        """ Log a message to the logging system

        :type message: str
        :param message: Message to write to the log
        :type level: str
        :param level: Log level (DEBUG, INFO, WARNING or ERROR)
        :returns: None
        """
        print('{service_name} - {level} - {message}'.format(
            service_name=self.name,
            level=level.upper(),
            message=message))


def register(service):
    """ Register a new service

    :type service: class
    :param service: Python class instance to add
    :returns: None
    """
    SERVICES.append(service)


def start():
    """ Start monitoring """
    for service in SERVICES:
        print(service.execute_all())

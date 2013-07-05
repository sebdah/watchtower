""" Service definition """
import time
import json
import signal

from watchtower import exceptions, status_codes


SERVICES = []


class Service(object):
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

    def add(self, name, monitor, interval=300, timeout=10, args=[], kwargs={}):
        """ Add a monitor to the monitoring list

        :type name: str
        :param name: Name of the monitor
        :type monitor: function
        :param monitor: A Python function to execute
        :type interval: int
        :param interval: How many seconds to sleep between each check
        :type timeout: int
        :param timeout: Timeout if the monitor havn't returned after n seconds
        :type args: list
        :param args: List of positional arguments to use
        :type kwargs: dict
        :param kwargs: Dictionary with keyword arguments
        :returns: None
        """
        self.monitors[name] = {
            'monitor': monitor,
            'interval': int(interval),
            'timeout': int(timeout),
            'args': args,
            'kwargs': kwargs
        }

        self.log('Added monitor "{monitor_name}"'.format(monitor_name=name))
        self.log(
            '{monitor_name} - interval: {interval}'.format(
                monitor_name=name,
                interval=interval),
            level='DEBUG')
        self.log(
            '{monitor_name} - timeout: {timeout}'.format(
                monitor_name=name,
                timeout=timeout),
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
                self.log(
                    '{monitor_name} not in check interval. Skipping.'.format(
                        monitor_name=name),
                    level='DEBUG')
                return None

            def timeout_handler(signum, frame):
                """ Timeout handler function

                :type signum: int
                :param signum: Signal number
                :type frame: Current stack frame
                """
                raise exceptions.TimeoutException()

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.monitors[name]['timeout'])

            try:
                return self.monitors[name]['monitor'](
                    *self.monitors[name]['args'],
                    **self.monitors[name]['kwargs'])
            except exceptions.TimeoutException:
                return {
                    'status': status_codes.ERROR,
                    'message': 'Monitor timed out after {:d} seconds'.format(
                        self.monitors[name]['timeout'])
                }

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
                results[monitor] = {
                    'status': result['status'],
                    'message': result['message']
                }

        self.log(
            'Results: \n{results}'.format(
                results=json.dumps(results, indent=4)),
            level='DEBUG')

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

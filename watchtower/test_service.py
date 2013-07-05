""" Testing the Service class """
from nose.tools import assert_equal, assert_in, assert_not_in

from watchtower import service


class TestService(service.Service):
    """ Test class for Service """

    def __init__(self):
        super(TestService, self).__init__('test')

    def test_add_monitor_to_list(self):
        """ Check that monitors are added to the monitor list """
        name = 'Disk space - /'

        def check_disk(rtn, disk='/'):
            return {
                'status': 0,
                'message': 'All is OK'
            }


        assert_not_in(name, self.monitors)
        self.add(
            name=name,
            monitor=check_disk,
            interval=10,
            args=['ok'])
        assert_in(name, self.monitors)

    def test_execute(self):
        """ Basic execution test """
        name = 'Disk space - /'

        def check_disk(rtn, disk='/'):
            return {
                'status': 0,
                'message': 'All is OK'
            }

        self.add(
            name=name,
            monitor=check_disk,
            interval=1,
            args='a')

        result = self.execute(name)
        assert result
        assert_equal(0, result['status'])
        assert_equal('All is OK', result['message'])

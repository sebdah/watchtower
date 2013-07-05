""" Testing the Service class """
import time

from nose.tools import assert_equal, assert_false, assert_in, assert_not_in

from watchtower import service, status_codes


class TestService(service.Service):
    """ Test class for Service """

    def __init__(self):
        super(TestService, self).__init__('TestService')

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

    def test_execute_all(self):
        """ Test execution of multiple monitors """
        def check_disk(disk='/'):
            return {
                'status': 0,
                'message': 'All is OK'
            }

        self.monitors = {}
        self.add(name='Check /', monitor=check_disk, interval=1)
        self.add(name='Check /mnt', monitor=check_disk, interval=1)

        result = self.execute_all()
        assert result
        assert_equal(2, len(result))

    def test_execute_none(self):
        """ Test to execute non-existing monitor """
        assert_false(self.execute('01823u4hfnsndiuf1y948uh'))

    def test_execute_timeout(self):
        """ Test execute timeouts """
        name = 'Disk space - /'

        def check_disk(rtn, disk='/'):
            time.sleep(2)
            return {
                'status': 0,
                'message': 'All is OK'
            }

        self.add(
            name=name,
            monitor=check_disk,
            interval=1,
            args='a',
            timeout=1)

        result = self.execute(name)
        assert result
        assert_equal(status_codes.ERROR, result['status'])
        assert_equal('Monitor timed out after 1 seconds', result['message'])

    def test_service_name(self):
        """ Test that the service name is set properly """
        assert_equal(self.name, 'TestService')

""" Testing the Service class """
from nose.tools import assert_in, assert_not_in

from watchtower import service


class TestService(service.Service):
    """ Test class for Service """

    def __init__(self):
        super(TestService, self).__init__('test')

    def test_add(self):
        """ Test the add function """
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


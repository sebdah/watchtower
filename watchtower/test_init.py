""" Test the __init__ methods """
from nose.tools import assert_in, assert_not_equal

import watchtower

def test_add_service():
    """ Test registering services """
    for service in watchtower.SERVICES:
        assert_not_equal(service.name, 'Frontend')

    watchtower.register(watchtower.Service(name='Frontend'))

    service_names = []
    for service in watchtower.SERVICES:
        service_names.append(service.name)
    assert_in('Frontend', service_names)

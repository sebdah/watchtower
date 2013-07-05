""" Init file for Watchtower """
from service import Service, SERVICES


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

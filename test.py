#!/usr/bin/env python
import watchtower

def check_disk(rtn, disk='/'):
    return rtn

service = watchtower.Service(name='Frontend')
service.add(
    name='Disk space - /',
    monitor=check_disk,
    interval=10,
    args=['ok'])
service.add(
    name='Disk space - /vol',
    monitor=check_disk,
    interval=10,
    args=['nok'],
    kwargs={'disk': '/vol'})

# Register services and start Watchtower
watchtower.register(service)
watchtower.start()

#!/usr/bin/env python
import time

import watchtower

def check_disk(rtn, disk='/'):
    return {
        'status': 0,
        'message': 'All is OK'
    }

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

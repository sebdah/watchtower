#!/usr/bin/env python
import time

import watchtower
from watchtower.monitors import check_disk


service = watchtower.Service(name='My Mac')
service.add(
    name='Disk space - /',
    monitor=check_disk.check_disk,
    interval=1,
    kwargs={
        'path': '/',
        'warning': 50
    })

# Register services and start Watchtower
watchtower.register(service)
watchtower.start()

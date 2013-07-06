""" Monitor checking disk usage """
import os
from collections import namedtuple


def check_disk(path='/', warning=80, critical=90):
    """ Check disk usage

    :type warning: int
    :param warning: Warning limit in %
    :type critical: int
    :param critical: critical limit in %
    """
    total, used, free = disk_usage(path)
    used_percent = float(used) / float(total)

    message = ('{used_percent:.2%} of {path} disk space is used '
        '(Total: {total_mb} MB, '
        'Used: {used_mb} MB, '
        'Free: {free_mb} MB)').format(
            used_percent=used_percent,
            path=path,
            total_mb=total / 1000 / 1000,
            used_mb=used / 1000 / 1000,
            free_mb=free / 1000 / 1000)

    used_percent = int(used_percent * 100.00)
    status_code = 0
    if used_percent >= critical:
        status_code = 2
    elif used_percent >= warning:
        status_code = 1

    return {
        'status_code': status_code,
        'message': message
    }


def disk_usage(path):
    """ Return disk usage statistics about the given path. UNIX ONLY!

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return (total, used, free)

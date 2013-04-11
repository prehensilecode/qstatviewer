#!/usr/bin/env python
"""
Misc. functions and global objects for qstatviewer
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import re, datetime

__version__ = '0.8.11'

jobstate_dict = {
    'Q': 'Queued', 
    'H': 'Held',
    'W': 'Waiting',
    'T': 'Transiting',
    'R': 'Running',
    'S': 'Suspended',
    'E': 'Exiting',
    'C': 'Completed',
    }

nodestate_dict = {
    'F': 'free',
    'B': 'busy',
    'O': 'offline',
    'E': 'job-exclusive',
    }

def pbstimestr_to_timedelta(pbstime):
    """Convert a Torque time string to a timedelta object"""
    t = [int(i) for i in pbstime.split(':')]
    return datetime.timedelta(hours=t[0], minutes=t[1], seconds=t[2])


def timedeltastr(pbstime):
    """Convert a cput or walltime into a compact printable string"""
    dayspat = re.compile('\ days?,')
    return dayspat.sub('d', str(pbstime))


def convert_memory(memstr=None, units=None):
    """
    Converts TORQUE memory strings, in the form, 'NNNNNNkb' to dict: {'qty': QTY, 'units': UNITS}
    """
    KILO = 1024.
    MEGA = 1048576.

    memkb = 0.

    bpat = re.compile('\d+b$')
    kbpat = re.compile('\d+kb$')
    mbpat = re.compile('\d+mb$')
    gbpat = re.compile('\d+gb$')
    
    if memstr:
        if bpat.match(memstr):
            memkb = float(memstr.split('b')[0]) / KILO
        elif kbpat.match(memstr):
            memkb = float(memstr.split('kb')[0])
        elif mbpat.match(memstr):
            memkb = float(memstr.split('mb')[0]) * KILO
        elif gbpat.match(memstr):
            memkb = float(memstr.split('gb')[0]) * MEGA

    if not units:
        if memkb < KILO:
            units = 'kB'
        elif memkb < MEGA:
            units = 'MB'
        else:
            units = 'GB'

    mem = {}
    if units == 'GB' or units == 'GiB' or units == 'gb':
        mem['units'] = 'GiB'
        mem['qty'] = memkb/(MEGA)
    elif units == 'MB' or units == 'MiB' or units == 'mb':
        mem['units'] = 'MiB'
        mem['qty'] = memkb/(KILO)
    elif units == 'kB' or units == 'kiB' or units == 'kb':
        mem['units'] = 'kiB'
        mem['qty'] = memkb
    return mem

    
if __name__ == '__main__':
    print convert_memory('1024000000kb')
    print convert_memory('1024000000kb', 'MiB')
    print convert_memory('1024000000kb', 'kB')

    print convert_memory('10b')
    print convert_memory('1000b')

    print convert_memory('10kb')
    print convert_memory('1000kb')

    print convert_memory('10mb')
    print convert_memory('1000mb')

    print convert_memory('10gb')
    print convert_memory('1000gb')


    td = datetime.timedelta(hours=5000, minutes=32, seconds=57)
    print 'td =', td
    print '   =', timedeltastr(td)

    t = '400:00:00'
    print 't =', t
    print '  =', pbstimestr_to_timedelta(t)


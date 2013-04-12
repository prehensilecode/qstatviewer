#!/usr/bin/env python
"""
Misc. functions and global objects for qstatviewer
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import os, sys, re, datetime

__version__ = '0.9.1'

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

    bpat = re.compile(r'(\d+\.?\d*)(b)$', re.I)
    kbpat = re.compile(r'(\d+\.?\d*)(ki?b)$', re.I)
    mbpat = re.compile(r'(\d+\.?\d*)(mi?b)$', re.I)
    gbpat = re.compile(r'(\d+\.?\d*)(gi?b)$', re.I)

    if memstr:
        bs = bpat.search(memstr)
        ks = kbpat.search(memstr)
        ms = mbpat.search(memstr)
        gs = gbpat.search(memstr)

        if bs:
            memkb = float(memstr.split(bs.group(2))[0]) / KILO
        elif kbpat.match(memstr):
            memkb = float(memstr.split(ks.group(2))[0])
        elif mbpat.match(memstr):
            memkb = float(memstr.split(ms.group(2))[0]) * KILO
        elif gbpat.match(memstr):
            memkb = float(memstr.split(gs.group(2))[0]) * MEGA
        else:
            sys.stderr.write('convert_memory(): cannot parse "{0}"\n'.format(memstr))
            raise Exception

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
    ms = '1024000000kb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print convert_memory(ms, 'MiB')
    print convert_memory(ms, 'kB')

    ms = '10b'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '10B'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '1000b'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '1000B'
    print('string = {0}'.format(ms))
    print convert_memory(ms)

    print ''
    ms = '10kb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '10kiB'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '1000kb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '1000kIb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)

    print ''
    ms = '10mb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '1000mib'
    print('string = {0}'.format(ms))
    print convert_memory(ms)

    print ''
    ms = '10gb'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print ''
    ms = '10giB'
    print('string = {0}'.format(ms))
    print convert_memory(ms)
    print('')

    td = datetime.timedelta(hours=5000, minutes=32, seconds=57)
    print 'td =', td
    print '   =', timedeltastr(td)

    t = '400:00:00'
    print 't =', t
    print '  =', pbstimestr_to_timedelta(t)


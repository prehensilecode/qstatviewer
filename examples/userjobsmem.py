#!/usr/bin/env python
"""
Prints out memory info on USER's jobs
"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University

import sys
import os
import datetime
import qstatviewer as qv

from optparse import OptionParser


def main(username):
    q = qv.QstatViewer()

    id = 'n/a'
    group = 'n/a'
    reqmem = 'n/a'
    usevm = 'n/a'

    userjobs = q.jobs_by_user(username)

    formatstr = "{id:<9} | {group:>14} |  {reqmem:>11.11} |  {usevm:>11.11}"
    print(formatstr.format(id="JOBID", group="GROUP", reqmem="REQ MEM", usevm="USED MEM"))
    print("-----------+----------------+----------------+---------------")
    for jobid,job in sorted(userjobs.iteritems()):
        id = jobid.split('.')[0]
        group = job.group
        reqmem = job.resource_list['mem'].pretty_print()
        if 'vmem' in job.resources_used:
            usevm  = job.resources_used['vmem'].pretty_print()
        print(formatstr.format(id=id, group=group, reqmem=reqmem, usevm=usevm))
    
if __name__ == '__main__':
    usage = """usage: %program username"""
    parser = OptionParser()
    (opt, args) = parser.parse_args()

    if not args:
        print("ERROR: must give username")
        sys.exit(1)

    main(args[0])

#!/usr/bin/env python
"""
Prints out memory info on USER's jobs
"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University

import sys
import os
import datetime
import getpass
import qstatviewer as qv

from optparse import OptionParser


def main(username):
    q = qv.QstatViewer()

    id = 'n/a'
    group = 'n/a'
    reqmem = 'n/a'
    usevm = 'n/a'
    nnodes = 0

    userjobs = q.jobs_by_user(username)

    print("{n} JOBS BY {u}:".format(n=len(userjobs), u=username))

    formatstr = "{id:<9} | {group:>14} | {nnodes:>7} |  {reqmem:>11.11} |  {usevm:>11.11}"
    print(formatstr.format(id="JOBID", group="GROUP", nnodes="N.NODES", reqmem="REQ MEM", usevm="USED MEM"))
    print("----------+----------------+---------+--------------+---------------")
    for jobid,job in sorted(userjobs.iteritems()):
        id = jobid.split('.')[0]
        group = job.group
        if 'hosts' in job.__dict__:
            nnodes = len(job.hosts)
        reqmem = job.resource_list['mem'].pretty_print()
        if 'vmem' in job.resources_used:
            usevm  = job.resources_used['vmem'].pretty_print()
        print(formatstr.format(id=id, group=group, nnodes=nnodes, reqmem=reqmem, usevm=usevm))
    
if __name__ == '__main__':
    usage = """usage: %prog [username]"""
    parser = OptionParser(usage)
    (opt, args) = parser.parse_args()

    if not args:
        args = [getpass.getuser()]

    main(args[0])


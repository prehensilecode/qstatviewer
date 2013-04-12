#!/usr/bin/env python
"""Emulates output of 'qstat -a'"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University


import sys, os, re, datetime
from qstatviewer import *


if __name__ == '__main__':
    qv = QstatViewer()

    dayspat = re.compile('\ days,')

    print('{0}:'.format(qv.pbsquery.server))
    print("                                                                    Req'd         Req'd          Req'd           Elap'd")
    print("Job ID       Username Queue    Jobname          SessID   NDS TSK    Memory        CPUTime   S    Walltime        Walltime")
    print("------------ -------- -------- ---------------- ------ ----- --- ----------  -------------- - -------------- --------------")

    for jobid, j in sorted(qv.jobs.iteritems()):
        nodect = j.resource_list['nodect']
        ntasks = j.resource_list['ncpus']
        mem    = j.resource_list['mem']
        cputstr = timedeltastr(j.resource_list['cput'])

        reqwtstr = timedeltastr(j.resource_list['walltime'])

        if j.state == 'R':
            if j.resources_used:
                elapse = timedeltastr(j.resources_used['walltime'])
        else:
            elapse = 'n/a'

        formatstr = "{jid:<12.12} {job.owner:<8.8} {job.queue:<8.8} {job.name:<16.16} {job.session_id:>6} {nodect:>5} {ntasks:>3} {mem:>11} {cput:>14} {job.job_state} {reqwt:>14} {elapse:>14}"
        print(formatstr.format(jid=j.id.split('.')[0], job=j, nodect=nodect, ntasks=ntasks, mem=mem.pretty_print(), cput=cputstr, reqwt=reqwtstr, elapse=elapse))


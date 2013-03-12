#!/usr/bin/env python
"""Emulates output of 'qstat -a'"""

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

import sys, os, re, datetime
from qstatviewer import *


if __name__ == '__main__':
    qv = QstatViewer()

    dayspat = re.compile('\ days,')

    print('{0}:'.format(qv.pbsquery.server))
    print("                                                                    Req'd        Req'd          Req'd           Elap'd")
    print("Job ID       Username Queue    Jobname          SessID   NDS TSK    Memory       CPUTime   S    Walltime        Walltime")
    print("------------ -------- -------- ---------------- ------ ----- --- ---------  -------------- - -------------- --------------")

    for jobid, j in sorted(qv.jobs.iteritems()):
        nodect = j.resource_list['nodect']
        ntasks = j.resource_list['ncpus']
        mem    = convert_memory(j.resource_list['mem'], 'gb')
        cputstr = timedeltastr(j.resource_list['cput'])

        reqwtstr = timedeltastr(j.resource_list['walltime'])

        if j.state == 'R':
            if j.resources_used:
                elapse = timedeltastr(j.resources_used['walltime'])
        else:
            elapse = 'n/a'

        formatstr = "{jid:<12.12} {job.owner:<8.8} {job.queue:<8.8} {job.name:<16.16} {job.session_id:>6} {nodect:>5} {ntasks:>3} {memqty:>6.2f} {memunits:>3} {cput:>14} {job.job_state} {reqwt:>14} {elapse:>14}"
        print(formatstr.format(jid=j.id.split('.')[0], job=j, nodect=nodect, ntasks=ntasks, memqty=mem['qty'], memunits=mem['units'], cput=cputstr, reqwt=reqwtstr, elapse=elapse))


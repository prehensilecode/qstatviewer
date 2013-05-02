#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University


import sys, os
import re
import datetime
import time
import qstatviewer as qv
from optparse import OptionParser

# NOTE: this is not working right

def main(jobidlist=None, t=60):
    global q

    print("     JOB ID     USER S CPUS NDS       ReqWT       Used WT")
    r_formatstr = "{id:>11} {o:>8} {s} {c:>4} {n:>3} {rwt:>12} {uwt:>12}"
    q_formatstr = "{id:>11} {o:>8} {s} {c:>4} {n:>3} {rwt:>12}"
    while True:
        for j in jobidlist:
            #job = q.get_job('.'.join([j, q.servername]))
            job = q.jobs['.'.join([j, q.servername])]
            if job:
                if job.state == 'R':
                    print(r_formatstr.format(id=j, 
                        o=job.owner.split('@')[0], 
                        s=job.state,
                        c=job.resource_list['ncpus'],
                        n=job.resource_list['nodect'],
                        rwt=job.resource_list['walltime'],
                        uwt=job.resources_used['walltime'], ))
                else:
                    print(q_formatstr.format(id=j, 
                        o=job.owner.split('@')[0],
                        s=job.state,
                        c=job.resource_list['ncpus'],
                        n=job.resource_list['nodect'],
                        rwt=job.resource_list['walltime'], ))
                time.sleep(t)
            else:
                print("No such job %s" % (j))
                sys.exit(1)

if __name__ == '__main__':
    usage = """usage: %prog [options] jobid [jobid ...]"""
    parser = OptionParser(usage)
    parser.add_option('-t', '--time', type='int', default=60,
                      help='polling interval in seconds (def. 60)')
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    q = qv.QstatViewer()

    main(jobidlist=args, t=options.time)


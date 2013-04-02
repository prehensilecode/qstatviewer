#!/usr/bin/env python
# Author: David Chin <dwchin . acm.org>

import sys
import os
import datetime
import time
import qstatviewer as qv
from optparse import OptionParser

def print_job_detail(q, jobid):
    jobid = '.'.join([jobid, q.servername])

    print("{0}:".format(jobid.split('.')[0]))
    for k,v in q.jobs[jobid].__dict__.iteritems():
        print("    {0:17.17}\t\t{1}".format(k, v))
    print("\n")


def main(q, jobid_list):
    jobid_list.sort()

    for jobid in jobid_list:
        print_job_detail(q, jobid)


if __name__ == '__main__':
    usage = "usage: %prog jobid [jobid ...]"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    q = qv.QstatViewer()

    main(q, args)


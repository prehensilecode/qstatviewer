#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>

# Copyright 2013 Wake Forest University

# Simple example of using the Job and QstatViewer classes

import sys, os
from optparse import OptionParser
import qstatviewer as qv

parser = OptionParser()
parser.add_option('-b', '--bare', action='store_true', dest='bare',
                  default=False, help='do not use color in output')

(options, args) = parser.parse_args()

q = qv.QstatViewer(debug_p=False)

print 'JOB ID              GROUP      USER   NODES'
print '======      =============  ========   ====='
tmpset = set()
sorted_jobids = sorted(q.jobs.keys())
for id in sorted_jobids:
    job = q.jobs[id]
    if job.job_state == 'R':
        print "{0:<11.11}".format(id.split('.')[0]), "{0:>13.13}".format(job.egroup), "{0:>8.8}".format(job.owner), ":",
        for h in job.exec_host:
            tmpset.add(h.split('/')[0])
        for h in tmpset:
            print h,
        print ''
        tmpset.clear()

print''
tmpset.clear()

RED = '\033[0;31m'
BOLDRED = '\033[1;31m'

GREEN = '\033[0;32m'
BOLDGREEN = '\033[1;32m'

YELLOW = '\033[0;33m'
BOLDYELLOW = '\033[1;33m'

BLUE = '\033[0;34m'
BOLDBLUE = '\033[1;34m'

PURPLE = '\033[0;35m'
BOLDPURPLE = '\033[1;35m'

CYAN = '\033[0;36m'
BOLDCYAN = '\033[1;36m'

WHITE = '\033[0;37m'
BOLDWHITE = '\033[1;37m'

BLACK = '\033[0;30m'
BOLDBLACK = '\033[1;30m'

DEF = '\033[0;00m'

END = '\033[0m'

print '  NODE      JOB IDS'
print '=========   ======='
sorted_nodenames = sorted(q.nodes.keys())
if not options.bare:
    red = RED
    green = GREEN
    end = END
else:
    red = ''
    green = ''
    end = ''

for nodename in sorted_nodenames:
    jobstr = ' '.join([j.split('.')[0] for j in sorted(q.nodes[nodename].unique_jobs)])
    if jobstr:
        print("{0}{1:>9.9} : {2}{3}".format(red, nodename, jobstr, end))
    else:
        print("{0}{1:>9.9} : {2}{3}".format(green, nodename, jobstr, end))

print ''

print '  NODE      USERS'
print '=========   ======='

for nodename in sorted_nodenames:
    node = q.nodes[nodename]
    userset = set()
    for j in node.unique_jobs:
        userset.add(q.jobs[j].owner)
    userstr = ' '.join(sorted(userset))
    if userstr:
        print("{0:>9.9} : {1}".format(nodename, userstr))


print '\nBYE'


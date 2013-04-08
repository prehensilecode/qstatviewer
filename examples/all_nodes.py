#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>

# Copyright 2013 Wake Forest University

import sys, os
import qstatviewer as qv

q = qv.QstatViewer(debug_p=False)

tmpset = set()
print 'NODE        JOB IDS'
print '=========   ======='
sorted_nodenames = sorted(q.nodes.keys())
for nodename in sorted_nodenames:
    node = q.nodes[nodename]
    jobstr = ' '.join(sorted(set([j.split('.')[0] for j in node.unique_jobs])))
    if not jobstr:
        jobstr = ''
    print("{0:>9.9} : {1}".format(nodename, jobstr))

print '\n\n'

print 'NODE        OCCUPIED PROCS'
print '=========   =============='
for nodename in sorted_nodenames:
    print("{0:>9.9}         {1}/{2}".format(nodename, len(q.nodes[nodename].jobs), q.nodes[nodename].ncpus))

print '\nBYE'


#!/usr/bin/env python

import sys
import os

from PBSQuery import PBSQuery

pq = PBSQuery('torque')
jobs = pq.getjobs()

print '# There are %d jobs\n' % (len(jobs))

for k,v in jobs.iteritems():
    v = dict(v)
    print k
    for l,w in v.iteritems():
        print '\t',l,'\t\t',w
    print '-----'



#!/usr/bin/env python

import sys
import os

from PBSQuery import PBSQuery

pq = PBSQuery('rhel6pbs.deac.wfu.edu')
nodes = pq.getnodes()

print '# There are %d nodes\n' % (len(nodes))

for k,v in nodes.iteritems():
    v = dict(v)
    print k
    for l,w in v.iteritems():
        print '\t',l,'\t\t',w
    print '-----'



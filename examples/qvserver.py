#!/usr/bin/env python
"""Print out all info in a QstatViewer instance"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University


import sys
import os
from optparse import OptionParser
import qstatviewer as qv

parser = OptionParser()
parser.add_option('-s', '--short', action='store_true', default=False,
                  help='brief info for each node')
options, args = parser.parse_args()

q = qv.QstatViewer()

print("Server: {s}".format(s=q.servername))
#print("Server properties:")
#for k,v in sorted(q.serverinfo.iteritems()):
#    print "    ", k, v

print("")
print("QstatViewer:")
for k,v in sorted(q.__dict__.iteritems()):
    if k != 'jobs' and k != 'nodes':
        print("    {0:18.18}\t\t{1}".format(k, v))


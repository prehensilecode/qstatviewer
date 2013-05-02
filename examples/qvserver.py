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

print("There are {0} nodes".format(len(q.nodes)))
print("")

for servername,serverinfo in sorted(q.serverinfo.iteritems()):
    print("Server: {server}".format(server=servername))
    for k,v in sorted(serverinfo.iteritems()):
        print "    ", k, v


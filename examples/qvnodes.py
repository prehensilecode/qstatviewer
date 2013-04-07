#!/usr/bin/env python
"""Print out all nodes in a QstatViewer instance"""

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US


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

if options.short:
    for nodename, node in sorted(q.nodes.iteritems()):
        print("{0}:".format(nodename))
        print "    Properties:", node.properties
        print "    NCPUS:", node.ncpus
else:
    for nodename, node in sorted(q.nodes.iteritems()):
        print("{0}:".format(nodename))
        for k,v in node.__dict__.iteritems():
            print("    {0:10.10}\t\t{1}".format(k, v))
        print("\n")



#!/usr/bin/env python
"""Print out all nodes in a QstatViewer instance"""

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US


import sys
import os
import qstatviewer as qv

q = qv.QstatViewer()

print("There are {0} nodes".format(len(q.nodes)))
print("")

for nodename,node in q.nodes.iteritems():
    print("{0}:".format(nodename))
    for k,v in node.__dict__.iteritems():
        print("    {0:10.10}\t\t{1}".format(k, v))
    print("\n")


#!/usr/bin/env python
"""Print out all jobs in a QstatViewer instance"""

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

import sys
import os
import qstatviewer as qv

q = qv.QstatViewer()

print("There are {0} jobs".format(len(q.jobs)))
print("")

for jobid,job in sorted(q.jobs.iteritems()):
    print("{0}:".format(jobid.split('.')[0]))
    for k,v in job.__dict__.iteritems():
        print("    {0:17.17}\t\t{1}".format(k, v))
    print("\n")


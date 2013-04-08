#!/usr/bin/env python
"""Print out all jobs in a QstatViewer instance"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University

import sys
import os
import qstatviewer as qv

q = qv.QstatViewer()

print("There are {0} jobs".format(len(q.jobs)))
print("")


for jobid, job in q.jobs.iteritems():
    print("{0}:".format(jobid.split('.')[0]))
    for k, v in job.__dict__.iteritems():
        print("    {0:17.17}\t\t{1}".format(k, v))
    print("\n")

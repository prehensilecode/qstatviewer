#!/usr/bin/env python
"""
Prints out single-node jobs requesting walltime >48 hrs running on Infiniband
"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University

import sys
import os
import datetime
import qstatviewer as qv

q = qv.QstatViewer()

ibnodes = q.nodes_with_property('infiniband')

id = ''
owner = ''
group = ''
reqwt = ''
usewt = ''

formatstr = "{n:<8} | {id:<9} | {owner:>8} | {group:>14} |  {reqwt:>13.13} |  {usewt:>13.13}"
print(formatstr.format(n="NODE", id="JOBID", owner="OWNER", group="GROUP", reqwt="REQ.WALL", usewt="CUR.WALL"))
print("---------+-----------+----------+----------------+----------------+---------------")
for nodename,node in sorted(ibnodes.iteritems()):
    if node.unique_jobs:
        for j in node.unique_jobs:
            id = q.jobs[j].id.split('.')[0]
            owner = q.jobs[j].owner
            group = q.jobs[j].group
            reqwt = q.jobs[j].resource_list['walltime']
            if reqwt > datetime.timedelta(hours=48):
                usewt = qv.timedeltastr(q.jobs[j].resources_used['walltime'])
                n_nodes = int(q.jobs[j].resource_list['nodes'].split(':')[0])
                if n_nodes == 1:
                    print(formatstr.format(n=nodename, id=id, owner=owner, group=group, reqwt=qv.timedeltastr(reqwt), usewt=usewt))


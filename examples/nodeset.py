#!/usr/bin/env python
"""
Prints info about a given set of nodes (hardcoded into source)
"""

# Author: David Chin <dwchin . acm.org>
# Copyright 2013 Wake Forest University

import sys
import os
import datetime
import qstatviewer as qv

q = qv.QstatViewer()

nodes_to_watch = ['bc12bl02', 'bc12bl04', 'bc12bl05', 'bc12bl06', 'bc12bl07', 'bc12bl08',
    'bc14bl01', 'bc14bl03', 'bc14bl04', 'bc14bl05', 'bc14bl07', 'bc14bl09']

nodeset = {}
for n in nodes_to_watch:
    nodeset[n] = q.nodes[n]

# print nodeset

id = ''
owner = ''
group = ''
reqwt = ''
usewt = ''

formatstr = "{n:<8} | {id:<9} | {owner:>8} | {group:>14} |  {reqwt:>13.13} |  {usewt:>13.13}"
print(formatstr.format(n="NODE", id="JOBID", owner="OWNER", group="GROUP", reqwt="REQ.WALL", usewt="CUR.WALL"))
print("---------+-----------+----------+----------------+----------------+---------------")
for nodename,node in sorted(nodeset.iteritems()):
    if node.unique_jobs:
        for j in node.unique_jobs:
            id = q.jobs[j].id.split('.')[0]
            owner = q.jobs[j].owner
            group = q.jobs[j].group
            reqwt = q.jobs[j].resource_list['walltime']
            if q.jobs[j].state == 'R':
                usewt = q.jobs[j].resources_used['walltime']
            print(formatstr.format(n=nodename, id=id, owner=owner, group=group, reqwt=qv.timedeltastr(reqwt), usewt=usewt))


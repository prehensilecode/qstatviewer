#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

import sys
import os
import qstatviewer as qv

q = qv.QstatViewer()

id = ''
owner = ''
group = ''
reqwt = ''
usewt = ''

formatstr = "{n:>9}: {id:>6} {owner:>8} {group:>14} {nodes:>16}  {reqwt:>10}  {usewt:>10}"
print(formatstr.format(n="NODE", id="JOBID", owner="OWNER", group="GROUP", nodes="REQ.NODES", reqwt="REQ.WALL", usewt="CUR.WALL"))
print("----------------------------------------------------------------------------------")
for nodename,node in q.nodes.iteritems():
    if node.unique_jobs:
        for j in node.unique_jobs:
            id = q.jobs[j].id.split('.')[0]
            owner = q.jobs[j].owner
            group = q.jobs[j].group
            reqwt = q.jobs[j].resource_list['walltime']
            usewt = q.jobs[j].resources_used['walltime']
            nodes = q.jobs[j].resource_list['nodes']
            n_nodes = int(q.jobs[j].resource_list['nodes'].split(':')[0])
            if n_nodes == 1:
                print(formatstr.format(n=nodename, id=id, owner=owner, group=group, nodes=nodes, reqwt=reqwt, usewt=usewt))


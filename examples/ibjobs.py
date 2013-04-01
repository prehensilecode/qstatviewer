#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

import sys
import os
import qstatviewer as qv

q = qv.QstatViewer()

ibnodes = q.nodes_with_property('infiniband')

id = ''
owner = ''
group = ''
reqwt = ''
usewt = ''

formatstr = "{n:<8}: {id:>6} {owner:>8} {group:>14}   {reqwt:>10}  {usewt:>10}"
print(formatstr.format(n="NODE", id="JOBID", owner="OWNER", group="GROUP", reqwt="REQ.WALL", usewt="CUR.WALL"))
print("-------------------------------------------------------------------")
for nodename,node in ibnodes.iteritems():
    if node.unique_jobs:
        #print("{0}:".format(nodename))
        #print("    {0}".format(node.unique_jobs))
        for j in node.unique_jobs:
            id = q.jobs[j].id.split('.')[0]
            owner = q.jobs[j].owner
            group = q.jobs[j].group
            reqwt = q.jobs[j].resource_list['walltime']
            usewt = q.jobs[j].resources_used['walltime']
            print(formatstr.format(n=nodename, id=id, owner=owner, group=group, reqwt=reqwt, usewt=usewt))
        #for k,v in node.__dict__.iteritems():
        #    print("    {0:11.11}\t\t{1}".format(k, v))
        #print("\n")


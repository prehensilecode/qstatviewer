#!/usr/bin/env python
"""
Prints details about given job
"""

# Author: David Chin <dwchin . acm.org>

# Copyright 2013 Wake Forest University

import sys
import os
import datetime
import time
import qstatviewer as qv
from optparse import OptionParser

def print_job_detail(q, jobid, options):
    jobid = '.'.join([jobid, q.servername])

    headnode_dict = {'bc103bl05.deac.wfu.edu': 'rhel6head1',
                     'bc103bl06.deac.wfu.edu': 'rhel6head2',
                     'bc103bl09.deac.wfu.edu': 'rhel6head3'}

    if jobid in q.jobs:
        print("{0}:".format(jobid.split('.')[0]))
        job = q.jobs[jobid]
        print "    Name:", job.name
        print "    Owner:", job.owner
        print "    Group:", job.group_list[0]
        print "    Owner node:", headnode_dict[job.owner_node]
        print "    Mail users:", job.mail_users
        if options.long:
            # euser and egroup are accessible to admin users only
            if job.euser:
                print "    Euser:", job.euser
                print "    Egroup:", job.egroup
        print "    State:", qv.jobstate_dict[job.state]
        print "    Resources requested:"
        #for k,v in job.resource_list.iteritems():
        #    print "        ", k, v
        print "         Nodes:       ", job.resource_list['nodes']
        print "         No. of nodes:", job.resource_list['nodect']
        print "         Mem:          {mem:>11}".format(mem=job.resource_list['mem'].pretty_print())
        print "         P.Mem:        {mem:>11}".format(mem=job.resource_list['pmem'].pretty_print())
        print "         CPU time:    ", qv.timedeltastr(job.resource_list['cput'])
        print "         Walltime:    ", qv.timedeltastr(job.resource_list['walltime'])
        if job.extra:
            print "         X:           ", job.extra
        if job.state == 'R':
            print "    Resources used:" 
            if job.resources_used:
                print "         Mem:          {mem:>11}".format(mem=job.resources_used['mem'].pretty_print())
                print "         V.Mem:        {mem:>11}".format(mem=job.resources_used['vmem'].pretty_print())
                print "         CPU time:    ", qv.timedeltastr(job.resources_used['cput'])
                print "         Walltime:    ", qv.timedeltastr(job.resources_used['walltime'])
            else:
                print "         Not yet available"

            hostlist = ' '.join(list(job.hosts))
            print "    Hosts:", hostlist

            fabricset = set()
            for h in job.hosts:
                fabricset.add(q.nodes[h].fabric)
            fabriclist = ','.join(fabricset)
            print "    Network:", fabriclist

            print "    Walltime remaining:", qv.timedeltastr(job.walltime_remaining)

            if options.nodes:
                nodeheadfmtstr = "    {name:>9}: {fabric:>3.3} {memphys:>9.9} {memavail:>9.9} {state:>6.6} {njobs:>2} {loadave:>4}"
                nodefmtstr = "    {name:>9}: {fabric:>3.3} {memphys:>9} {memavail:>9} {state:>6.6} {njobs:>2} {loadave:>4.1f}"
                print(nodeheadfmtstr.format(name="NAME", fabric="FABRIC", memphys="PHYSMEM", memavail="AVAILMEM", state="STATE", njobs="NJOBS", loadave="LOADAVE"))
                for h in job.hosts:
                    print_node_detail(q, h, nodefmtstr)

            if options.long:
                print "    Submit host:", job.submit_host
                print "    Submit args:", job.submit_args
                if job.hashname:
                    print "    Hash name:", job.hashname
                print "    Working dir:", job.init_work_dir
                print "    Output path:", job.output_path
                if len(job.variable_list):
                    print "    Variable list:"
                    for k,v in job.variable_list.iteritems():
                        print "        {k:<13}: {v}".format(k=k, v=v[0])
                print "    Error path:", job.error_path
                print "    Session ID:", job.session_id
                if job.substate:
                    print "    Substate:", job.substate
                if job.queue_rank:
                    print "    Queue rank:", job.queue_rank
                print "    Rerunnable:", job.rerunnable
                print "    Fault-tolerant:", job.fault_tolerant
                print "    Join path:", job.join_path
                print "    Keep files:", job.keep_files
                print "    Mail points:", job.mail_points
                print "    Exec host:", job.exec_host
                print "    Ctime:", job.ctime
                print "    Etime:", job.etime
                print "    Qtime:", job.qtime
                print "    Mtime:", job.mtime
                print "    Start time:", job.start_time
    else:
        print "No such job id:", jobid
        sys.exit(1)


def print_node_detail(q, nodename, fmtstr):
    node = q.nodes[nodename]
    name = node.name
    fabric = node.fabric
    memphys = node.physmem
    memavail = node.availmem
    state = node.state
    njobs = len(node.jobs)
    loadave = node.loadave
    print(fmtstr.format(name=name, fabric=fabric, memphys=memphys, 
        memavail=memavail, state=state, njobs=njobs, loadave=loadave))

def main(q, jobid_list, options):
    jobid_list.sort()

    for jobid in jobid_list:
        print_job_detail(q, jobid, options)
        print ""


if __name__ == '__main__':
    usage = """usage: %prog jobid [jobid ...]
    Show detailed information about given jobs
    """
    parser = OptionParser(usage)
    parser.add_option('-l', '--long', action='store_true', dest='long',
                      default=False, help='long output')
    parser.add_option('-n', '--nodes', action='store_true', dest='nodes',
                      default=False, help='show information about nodes occupied by job(s)')

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    q = qv.QstatViewer()

    main(q, args, options)


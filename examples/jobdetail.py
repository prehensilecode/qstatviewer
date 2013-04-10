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
        mem = qv.convert_memory(job.resource_list['mem'])
        print "         Mem:          {qty:>6.2f} {units:3}".format(qty=mem['qty'], units=mem['units'])
        pmem = qv.convert_memory(job.resource_list['pmem'])
        print "         P.Mem:        {qty:>6.2f} {units:3}".format(qty=pmem['qty'], units=pmem['units'])
        print "         CPU time:    ", qv.timedeltastr(job.resource_list['cput'])
        print "         Walltime:    ", qv.timedeltastr(job.resource_list['walltime'])
        if job.extra:
            print "         X:           ", job.extra
        if job.state == 'R':
            print "    Resources used:" 
            #for k,v in job.resources_used.iteritems():
            #    print "        ", k, v
            if job.resources_used:
                mem = qv.convert_memory(job.resources_used['mem'])
                print "         Mem:          {qty:>6.2f} {units:3}".format(qty=mem['qty'], units=mem['units'])
                vmem = qv.convert_memory(job.resources_used['vmem'])
                print "         V.Mem:        {qty:>6.2f} {units:3}".format(qty=vmem['qty'], units=vmem['units'])
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
            print "    Walltime remaining:", datetime.timedelta(seconds=job.walltime_remaining)
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
                        #print "       ", k, ":", v[0]
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


def main(q, jobid_list, options):
    jobid_list.sort()

    for jobid in jobid_list:
        print_job_detail(q, jobid, options)
        print ""


if __name__ == '__main__':
    usage = "usage: %prog jobid [jobid ...]"
    parser = OptionParser(usage)
    parser.add_option('-l', '--long', action='store_true', dest='long',
                      default=False, help='long output')

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    q = qv.QstatViewer()

    main(q, args, options)


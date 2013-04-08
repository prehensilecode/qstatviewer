#!/usr/bin/env python
# Author: David Chin <dwchin . acm.org>

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
        #for k,v in job.__dict__.iteritems():
        #    print("    {0:17.17}\t\t{1}".format(k, v))
        print "    Owner:", job.owner
        print "    Group:", job.group_list[0]
        print "    Owner node:", headnode_dict[job.owner_node]
        print "    Resources requested:"
        #for k,v in job.resource_list.iteritems():
        #    print "        ", k, v
        print "         Nodes:       ", job.resource_list['nodes']
        print "         No. of nodes:", job.resource_list['nodect']
        mem = qv.convert_memory(job.resource_list['mem'])
        print "         Mem:          {0:>6.2f} {1:3}".format(mem['qty'], mem['units'])
        pmem = qv.convert_memory(job.resource_list['pmem'])
        print "         P.Mem:        {0:>6.2f} {1:3}".format(pmem['qty'], pmem['units'])
        print "         CPU time:    ", qv.timedeltastr(job.resource_list['cput'])
        print "         Walltime:    ", qv.timedeltastr(job.resource_list['walltime'])
        if job.extra:
            print "         X:           ", job.extra
        print "    State:", qv.jobstate_dict[job.state]
        if job.state == 'R':
            print "    Resources used:" 
            #for k,v in job.resources_used.iteritems():
            #    print "        ", k, v
            if job.resources_used:
                mem = qv.convert_memory(job.resources_used['mem'])
                print "         Mem:      {0:>6.2f} {1:3}".format(mem['qty'], mem['units'])
                vmem = qv.convert_memory(job.resources_used['vmem'])
                print "         V.Mem:    {0:>6.2f} {1:3}".format(vmem['qty'], vmem['units'])
                print "         CPU time:", qv.timedeltastr(job.resources_used['cput'])
                print "         Walltime:", qv.timedeltastr(job.resources_used['walltime'])
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
    parser.add_option('-s', '--short', action='store_true',
                      default=False, help='short output')

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    q = qv.QstatViewer()

    main(q, args, options)


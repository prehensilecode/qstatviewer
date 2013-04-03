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

    print("{0}:".format(jobid.split('.')[0]))
    job = q.jobs[jobid]
    #for k,v in job.__dict__.iteritems():
    #    print("    {0:17.17}\t\t{1}".format(k, v))
    print "    Owner:", job.owner
    print "    Group:", job.group_list[0]
    print "    Owner node:", headnode_dict[job.owner_node]
    print "    Resource list:", job.resource_list
    print "    State:", job.state
    if job.state == 'R':
        print "    Resources used:", job.resources_used
        hostlist = ' '.join(list(job.hosts))
        print "    Hosts:", hostlist
        print "    Walltime remaining:", datetime.timedelta(seconds=job.walltime_remaining)
    print("\n")


def main(q, jobid_list, options):
    jobid_list.sort()

    for jobid in jobid_list:
        print_job_detail(q, jobid, options)


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


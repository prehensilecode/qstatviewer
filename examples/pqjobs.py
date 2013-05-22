#!/usr/bin/env python
import sys
import os
import re

from PBSQuery import PBSQuery

def main():
    pq = PBSQuery()
    jobsdict = pq.getjobs()
    for jobid, job in sorted(jobsdict.iteritems()):
        print jobid
        for k, v in job.iteritems():
            print '    ', k, v
        print ''

if __name__ == '__main__':
    main()


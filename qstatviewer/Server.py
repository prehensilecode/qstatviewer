#!/usr/bin/env python
"""
Encapsulates information about Torque queues
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import sys, os, re, string, copy, datetime
import pickle

from PBSQuery import PBSQuery
from StringIO import StringIO

from qstatviewer.config import __version__, pbstimestr_to_timedelta
from qstatviewer.Memory import Memory

# Some of the node properties here are defined in the Torque source:
#    src/resmom/linux/mom_mach.c

class Server:
    """
    Encapsulates information about a TORQUE server
    """
    def __init__(self, name=None, pbsserver_dict=None):
        if name:
            self.name = name
        elif pbsserver_dict:
            self.name = pbsserver_dict['server']
        else:
            print('ERROR: cannot find server name')
            raise
            
        for k,v in sorted(pbsserver_dict[self.name].iteritems()):
            if len(v) == 1:
                self.__dict__[k] = v[0]
            else:
                self.__dict__[k] = v

        # fix up the values
        self.next_job_number     = int(self.next_job_number)
        self.total_jobs          = int(self.total_jobs)
        self.node_check_rate     = int(self.node_check_rate)
        self.scheduler_iteration = int(self.scheduler_iteration)
        self.tcp_timeout         = int(self.tcp_timeout)

        self.log_events = int(self.log_events)

        self.scheduling       = (self.scheduling == 'True')
        self.query_other_jobs = (self.query_other_jobs == 'True')

        states = self.state_count.strip().split(' ')
        self.state_count = {}
        for s in states:
            (st, val) = s.split(':')
            self.state_count[st] = int(val)

        for res,val in self.resources_assigned.iteritems():
            if res == 'mem' or res == 'vmem' or res == 'pmem':
                self.resources_assigned[res] = Memory(self.resources_assigned[res][0])
            elif res == 'ncpus' or res == 'nodect':
                self.resources_assigned[res] = int(self.resources_assigned[res][0])

        for res,val in self.resources_default.iteritems():
            if res == 'mem' or res == 'vmem' or res == 'pmem':
                self.resources_default[res] = Memory(self.resources_default[res][0])
            elif res == 'cput' or res == 'walltime':
                self.resources_default[res] = pbstimestr_to_timedelta(self.resources_default[res][0])


    def __str__(self):
        outlist = ['Server: {0}'.format(self.name), '\n',
                   '    ACL hosts:    {0}'.format(self.acl_hosts), '\n',
                   '    Scheduling:   {0}'.format(self.scheduling), '\n',
                   '    Managers:     {0}'.format(self.managers), '\n',
                   "    Auth'd users: {0}".format(self.authorized_users), '\n',
                   '    Submit hosts: {0}'.format(self.submit_hosts), '\n',
                   '    Next job no.: {0}'.format(self.next_job_number), '\n',
                   '    Log events:   {0}'.format(self.log_events), '\n',
                   '    Mail from:    {0}'.format(self.mail_from), '\n',
                   '    Query other jobs: {0}'.format(self.query_other_jobs), '\n',
                   '    Resources default: {0}'.format(self.resources_default), '\n',
                   '    Scheduler iteration: {0}'.format(self.scheduler_iteration), '\n',
                   '    Node check rate: {0}'.format(self.node_check_rate), '\n',
                   '    TCP timeout: {0}'.format(self.tcp_timeout), '\n',
                  ]
        retstr = "".join(outlist)
        return retstr


if __name__ == '__main__':
    pq = PBSQuery()

    server = Server(name=pq.server, pbsserver_dict=pq.get_serverinfo())

    print server
    

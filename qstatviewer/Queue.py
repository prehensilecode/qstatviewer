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

from qstatviewer.config import __version__
from qstatviewer.Memory import Memory

# Some of the node properties here are defined in the Torque source:
#    src/resmom/linux/mom_mach.c

class Queue:
    """
    Encapsulates information about a queue in a TORQUE cluster
    """
    def __init__(self, name=None, pbsqueue_dict=None):
        if name:
            self.name = name
        elif pbsqueue_dict:
            self.name = pbsqueue_dict['name']
        else:
            print('ERROR: cannot find queue name')
            raise

        self.queue_type = pbsqueue_dict['queue_type'][0]

        if self.queue_type == 'Routing':
            self.route_destinations = pbsqueue_dict['route_destinations']
        elif self.queue_type == 'Execution':
            queue_props = ['max_user_queuable', 'max_queuable', 'total_jobs']
            for p in queue_props:
                 self.__dict__[p] = int(pbsqueue_dict[p][0])

            self.resources_default = {}
            for k,v in pbsqueue_dict['resources_default'].iteritems():
                if k == 'arch':
                    self.resources_default[k] = v[0]

            if 'resources_assigned' in pbsqueue_dict:
                self.resources_assigned = {}
                for k,v in pbsqueue_dict['resources_assigned'].iteritems():
                    if k == 'mem' or k == 'vmem':
                        self.resources_assigned[k] = Memory(v[0])
                    elif k == 'ncpus' or k == 'nodect':
                        self.resources_assigned[k] = int(v[0])

        if 'acl_groups' in pbsqueue_dict:
            self.acl_groups = pbsqueue_dict['acl_groups']

        if 'mtime' in pbsqueue_dict:
            self.mtime = datetime.datetime.fromtimestamp(int(pbsqueue_dict['mtime'][0]))

        for p in ['started', 'enabled', 'acl_group_enable']:
            if p in pbsqueue_dict:
                if pbsqueue_dict[p][0] == 'True':
                    self.__dict__[p] = True
                else:
                    self.__dict__[p] = False

        if 'state_count' in pbsqueue_dict:
            self.state_count = {}
            state_counts = pbsqueue_dict['state_count'][0].strip().split(' ')
            for s in state_counts:
                name, count = s.split(':')
                self.state_count[name] = int(count)



    def __str__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    pq = PBSQuery()
    queues = {}
    for k,v in sorted(pq.getqueues().iteritems()):
        queues[k] = Queue(name=k, pbsqueue_dict=v)


    for queuename, queue in sorted(queues.iteritems()):
        print queuename, ':', queue


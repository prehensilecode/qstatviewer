#!/usr/bin/env python

# Author: David Chin <dwchin@acm.org>

# Copyright 2013 Wake Forest University

import sys, os, re, string, copy
import pickle

from PBSQuery import PBSQuery
from StringIO import StringIO

from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory

class Node:
    """
    Encapsulates information about a node in a TORQUE cluster
    """
    def __init__(self, name=None, pbsnodes_dict=None, debug_p=False):
        self.debug_p = debug_p

        if self.debug_p:
            print('FOOBAR: ', jobstate_dict)

        if not name:
            print('ERROR: node name not given')
            raise

        pbsnodes_dict = dict(pbsnodes_dict)

        self.name = name
        self.state = pbsnodes_dict['state'][0] # string
        self.ntype = pbsnodes_dict['ntype'][0] # string -- node type
        self.np = int(pbsnodes_dict['np'][0])  # integer -- no. of processors
        self.properties = pbsnodes_dict['properties']  # list of node properties/features (strings)
        self.opsys = ''          # string -- OS
        self.uname = ''          # string -- `uname -a`
        self.sessions = ''       # list of integers -- session IDs
        self.nsessions = ''      # integer -- number of sessions
        self.nusers = 0          # integer - no. of users
        self.idletime = 0        # integer -- no. of seconds idle (?)
        self.totmem = 0          # integer -- total memory in kb
        self.availmem = 0        # integer -- available memory in kb
        self.physmem = 0         # integer -- physical memory in kb
        self.ncpus = 8           # integer -- no. of processors
        self.loadave = 0.        # float -- load average
        self.netload = 0         # integer -- network load (?)
        self.jobs = []           # list of jobs running on node
                                 #    we will use the Job class to find this because the
                                 #    time difference between calling qstat -f and pbsnodes -a
                                 #    may mean the per-node list of jobs may have changed
                                 #    ARGH. But if the job list has changed, the state may 
                                 #    also have changed. So, just get it from pbsnodes -a
        self.unique_jobs = set()
        self.varattr = ''        # list - non-functional - see http://www.clusterresources.com/torquedocs21/a.cmomconfig.shtml
                                 #        and http://www.clusterresources.com/pipermail/torquedev/2008-October/001228.html
        self.rectime = 0         # integer -- ??

        self.name = name

        # figure out clan from name
        self.clan = ''
        clanpat = re.compile('^bc(\d{2})')
        gridpat = re.compile('^bcg(\d{2})')
        cp = clanpat.search(self.name)
        gp = gridpat.search(self.name)
        if cp:
            if self.debug_p:
                print 'cp.group(1) = ', cp.group(1)
            self.clan = ''.join(['clan', cp.group(1)])

        if gp:
            if self.debug_p:
                print 'gp.group(1) = ', gp.group(1)
            self.clan = ''.join(['grid', gp.group(1)])

        # figure out fabric from properties
        self.fabric = ''
        if 'ethernet' in self.properties:
            self.fabric = 'ethernet'
        elif 'infiniband' in self.properties:
            self.fabric = 'infiniband'

        # if node has not been imaged, but is entered in qmgr,
        # then it won't have a 'status' key

        if 'status' in pbsnodes_dict:
            self.sessions = pbsnodes_dict['status']['sessions'][0].split(' ')
            self.sessions = [int(s) for s in self.sessions]
            self.nsessions = int(pbsnodes_dict['status']['nsessions'][0])
            self.nusers = int(pbsnodes_dict['status']['nusers'][0])
            self.opsys = pbsnodes_dict['status']['opsys'][0]
            self.physmem = int(pbsnodes_dict['status']['physmem'][0].split('kb')[0])
            self.availmem = int(pbsnodes_dict['status']['availmem'][0].split('kb')[0])
            self.varattr = pbsnodes_dict['status']['varattr']
            self.netload = int(pbsnodes_dict['status']['netload'][0])
            self.uname = pbsnodes_dict['status']['uname'][0]
            self.idletime = int(pbsnodes_dict['status']['idletime'][0])
            self.totmem = int(pbsnodes_dict['status']['totmem'][0].split('kb')[0])

            self.size = pbsnodes_dict['status']['size'][0].split(':')
            self.size[0] = int(self.size[0].split('kb')[0])
            self.size[1] = int(self.size[1].split('kb')[0])

            self.arch = pbsnodes_dict['status']['arch'][0]
            self.rectime = int(pbsnodes_dict['status']['rectime'][0])
            self.loadave = float(pbsnodes_dict['status']['loadave'][0])
            
            unique_jobs = set()
            if 'jobs' in pbsnodes_dict:
                self.jobs = pbsnodes_dict['jobs']
                if pbsnodes_dict['jobs']:
                    for j in pbsnodes_dict['jobs']:
                        unique_jobs.add(j.split('/')[1])
                self.unique_jobs = unique_jobs


    def free_cpus(self):
        """Returns the number of available CPUs"""

        retval = self.ncpus
        if not self.state == 'free':
            retval = self.ncpus - len(self.jobs)
        return retval


    def __str__(self):
        return str(self.__dict__)
        

if __name__ == '__main__':
    pq = PBSQuery()
    nodes = {}
    for k,v in pq.getnodes().iteritems():
        nodes[k] = Node(name=k, pbsnodes_dict=dict(v))

    for k,v in nodes.iteritems():
        print k, ': ', v
        print "Name = %s, State = %s, Free CPUs = %d, Clan = %s, Fabric = %s" % (v.name, v.state, v.free_cpus(), v.clan, v.fabric)
        print '----'


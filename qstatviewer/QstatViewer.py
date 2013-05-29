#!/usr/bin/env python
"""
Encapsulates information about Torque queue and resources. Wraps
around PBSQuery class, and expands its nested lists to be more
easily useable.
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import sys, os, re, string, copy
import shlex
import subprocess
import pickle
import datetime

from PBSQuery import PBSQuery
from StringIO import StringIO

from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory, timedeltastr, pbstimestr_to_timedelta
from qstatviewer.Node import Node
from qstatviewer.Job import Job
from qstatviewer.Node import Memory
from qstatviewer.Queue import Queue
from qstatviewer.Server import Server

class QstatViewer:
    """
    Presents a nicer (?) interface to PBSQuery
    The two main member objects are:
    * jobs -- a dictionary with job ID (as str) as the key, 
              and the corresponding Job object as the value
    * nodes -- a dictionary with node name as the key, 
               and a set of corresponding job IDs (of jobs 
               running on node)
    """
    def __init__(self, pbs_server=None, debug_p=False):
        """Creates a QstatViewer object. Arguments:
           - pbs_server : FQDN of the TORQUE server to query (string)"""
        self.debug_p = debug_p

        self.nodes = {}
        self.jobs = {}
        self.queues = {}

        self.pbsquery = PBSQuery(pbs_server)

        self.servername = self.pbsquery.get_server_name()

        self.__make_server()
        self.__make_queues()
        self.__make_jobs()
        self.__make_nodes()


    def __make_nodes(self):
        """Make dict with node names as keys, and list of job objects as values"""

        # make list of jobids running on the node
        #node_jobs = {}
        #for jobid,job in self.jobs.iteritems():
        #    if job.exec_host:
        #        for node_cpu in job.exec_host:
        #            node = node_cpu.split('/')[0]
        #            if node not in node_jobs:
        #                node_jobs[node] = []
        #            else:
        #                node_jobs[node].append(jobid)

        rawnodes = self.pbsquery.getnodes()
        for n,s in rawnodes.iteritems():
            self.nodes[n] = Node(name=n, pbsnodes_dict=dict(s), debug_p=self.debug_p)


    def __make_jobs(self):
        """Make dict with job IDs as keys, and job properties as values"""
        rawjobs = self.pbsquery.getjobs()
        for j,p in rawjobs.iteritems():
            self.jobs[j] = Job(id=j, pbsjobs_dict=dict(p), debug_p=self.debug_p)

    def __make_queues(self):
        """make dict with queue names as keys, and queue properties as values"""
        rawqueues = self.pbsquery.getqueues()
        for q,p in rawqueues.iteritems():
            self.queues[q] = Queue(name=q, pbsqueue_dict=p)

    def __make_server(self):
        self.__serverinfo = self.pbsquery.get_serverinfo()[self.servername]
        if self.debug_p:
            print 'FOOBAR: self.serverinfo =', self.__serverinfo
        for k,v in self.__serverinfo.iteritems():
            self.__dict__[k] = None
            if k == 'state_count':
                # Example of state_count: Transit:0 Queued:-6458 Held:6383 Waiting:0 Running:964 Exiting:0
                self.__dict__[k] = {}
                vals = v[0].strip().split(' ')
                for state in vals:
                    statename = state.split(':')[0]
                    stateval  = int(state.split(':')[1])
                    self.__dict__[k][statename] = stateval
            elif k == 'resources_default':
                v['mem'] = Memory(v['mem'][0])
                v['pmem'] = Memory(v['pmem'][0])
                v['cput'] = pbstimestr_to_timedelta(v['cput'][0])
                v['walltime'] = pbstimestr_to_timedelta(v['walltime'][0])
                self.__dict__[k] = v
            elif k == 'resources_assigned':
                if 'mem' in v:
                    v['mem'] = Memory(v['mem'][0])

                if 'vmem' in v:
                    v['vmem'] = Memory(v['vmem'][0])

                if 'ncpus' in v:
                    v['ncpus'] = int(v['ncpus'][0])
                
                if 'nodect' in v:
                    v['nodect'] = int(v['nodect'][0])

                self.__dict__[k] = v
            elif k == 'scheduling' or k == 'query_other_jobs':
                if v[0] == 'True':
                    v[0] = True
                elif v[0] == 'False':
                    v[0] = False
                self.__dict__[k] = v[0]
            elif k == 'scheduler_iteration':
                self.__dict__[k] = datetime.timedelta(seconds=int(v[0]))
            elif k == 'next_job_number' or k == 'node_check_rate' or k == 'tcp_timeout' or k == 'total_jobs':
                self.__dict__[k] = int(v[0])
            elif len(v) == 1:
                self.__dict__[k] = v[0]
            else:
                self.__dict__[k] = v



    def get_job(self, jobid):
        """Queries the queue for jobid"""
        j = self.pbsquery.getjob(jobid)
        if self.debug_p:
            print 'ALOHA: ',
            print j.__dict__['data']

        if 'data' in j.__dict__:
            return Job(id=jobid, pbsjobs_dict=dict(j), debug_p=self.debug_p)
        else:
            return None

    def jobs_by_user(self, username=None):
        """Returns a dict of jobs (keyed by jobid) belonging to username"""
        retval = {}
        if not username:
            retval = None
        else:
            for jobid,job in self.jobs.iteritems():
                if job.owner == username:
                    retval[jobid] = job
        return retval

    def nodes_with_property(self, prop):
        """Returns a dict of nodes (keyed by nodename) having the given property string"""
        retval = {}
        if prop:
            for nodename,node in self.nodes.iteritems():
                if prop in node.properties:
                    retval[nodename] = node
        else:
            retval = self.nodes
        return retval

    def nodes_in_clan(self, clan):
        """Returns a dict of nodes (keyed by nodename) belonging to the given clan"""
        retval = {}
        if clan:
            for nodename,node in self.nodes.iteritems():
                if clan == node.clan:
                    retval[nodename] = node
        else:
            retval = self.nodes
        return retval

    def __unicode__(self):
        if self.debug_p:
            print 'FOOBAR: type(self.jobs) =', type(self.jobs)
            print 'FOOBAR: self.jobs =', self.jobs
        job_dict_list = []
        for k,v in self.jobs.iteritems():
            job_dict_list.append(str(v))
        return str(job_dict_list)

    def __str__(self):
        return self.__unicode__()


if __name__ == '__main__':
    qv = QstatViewer(debug_p=False)
    j = qv.get_job('296561')
    print j


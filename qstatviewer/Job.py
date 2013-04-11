#!/usr/bin/env python
"""
Encapsulates information about Torque jobs
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University


import sys, os, re, string, copy
import datetime
import pickle

from PBSQuery import PBSQuery
from StringIO import StringIO

from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory, pbstimestr_to_timedelta
from qstatviewer.Memory import Memory

### This does not handle job arrays:
### - array jobs have two more entries: job_array_request, job_array_id, and 
### - array jobs do not have Hold_Types
### - array jobs Variable_List have a PBS_ARRAY_ID

# See ../prototyping/nonarray_job.txt for an example of a non-array job output
# See ../prototyping/array_job.txt for an example of an array job output


# There are differences in the job properties that an admin user
# can see vs. a non-admin user. An admin user can see these 7 additional
# fields in pbsjobs_dict:
#   substate
#   Variable_List
#   euser
#   egroup
#   hashname
#   queue_rank
#   queue_type



class Job:
    """
    Encapsulates information about jobs in a TORQUE cluster
    """
    def __init__(self, id=None, pbsjobs_dict=None, debug_p=False):
        self.debug_p = debug_p

        if not id:
            raise

        #self.__dict__ = pbsjobs_dict
        self.__pbsjobs_dict = pbsjobs_dict
        self.id = id
        self.name = pbsjobs_dict['Job_Name'][0]
        self.owner = pbsjobs_dict['Job_Owner'][0].split('@')[0]
        self.owner_node = pbsjobs_dict['Job_Owner'][0].split('@')[1]
        self.job_state = pbsjobs_dict['job_state'][0]
        self.state = self.job_state
        self.queue = pbsjobs_dict['queue'][0]
        self.server = pbsjobs_dict['server'][0]
        self.checkpoint = pbsjobs_dict['Checkpoint'][0]

        self.ctime = datetime.datetime.fromtimestamp(int(pbsjobs_dict['ctime'][0]))

        self.error_path = pbsjobs_dict['Error_Path'][0]

        self.init_work_dir = pbsjobs_dict['init_work_dir'][0]

        if 'exec_host' in pbsjobs_dict:
            self.exec_host = pbsjobs_dict['exec_host'][0].split('+')
            self.hosts = self.__list_unique_hosts()
        else:
            self.exec_host = None


        self.is_array_job = ('job_array_request' in pbsjobs_dict)
        if self.is_array_job:
            self.job_array_request = pbsjobs_dict['job_array_request']
            self.job_array_id = pbsjobs_dict['job_array_id']
        else:
            if pbsjobs_dict['Hold_Types'][0] == 'n':
                self.hold_types = False
            elif pbsjobs_dict['Hold_Types'][0] == 'y':
                self.hold_types = True
            else:
                raise "Don't know what Hold_Types this is"

        self.group_list = pbsjobs_dict['group_list']
        self.group = self.group_list[0]
        self.join_path = pbsjobs_dict['Join_Path'][0]

        if pbsjobs_dict['Keep_Files'][0] == 'y':
            self.keep_files = True
        elif pbsjobs_dict['Keep_Files'][0] == 'n':
            self.keep_files = False
        else:
            raise "Don't know what Keep_Files this is"

        self.mail_points = pbsjobs_dict['Mail_Points'][0]

        if 'Mail_Users' in pbsjobs_dict:
            self.mail_users = pbsjobs_dict['Mail_Users'][0]
        else:
            self.mail_users = None

        self.mtime = datetime.datetime.fromtimestamp(int(pbsjobs_dict['mtime'][0]))

        self.output_path = pbsjobs_dict['Output_Path'][0]
        self.priority = int(pbsjobs_dict['Priority'][0])

        self.qtime = datetime.datetime.fromtimestamp(int(pbsjobs_dict['qtime'][0]))

        
        # Yes, it's misspelled
        if pbsjobs_dict['Rerunable'][0] == 'True':
            self.rerunnable = True
        elif pbsjobs_dict['Rerunable'][0] == 'False':
            self.rerunnable = False
        else:
            raise "Don't know what Rerunable this is"

        # requested resources
        self.resource_list = pbsjobs_dict['Resource_List']
        self.resource_list['nodect'] = int(self.resource_list['nodect'][0])
        if 'ncpus' in self.resource_list:
            self.resource_list['ncpus'] = int(self.resource_list['ncpus'][0])
        else:
            self.resource_list['ncpus'] = self.__count_ncpus()
        self.ncpus = self.resource_list['ncpus']
        self.resource_list['walltime'] = pbstimestr_to_timedelta(self.resource_list['walltime'][0])
        self.resource_list['cput'] = pbstimestr_to_timedelta(self.resource_list['cput'][0])
        self.resource_list['mem'] = Memory(self.resource_list['mem'][0])
        self.resource_list['pmem'] = Memory(self.resource_list['pmem'][0])
        self.resource_list['arch'] = self.resource_list['arch'][0]
        self.resource_list['nodes'] = self.resource_list['nodes'][0]

        # resource_list['neednodes'] seems to only be available to admin users
        if 'neednodes' in self.resource_list:
            self.resource_list['neednodes'] = self.resource_list['neednodes'][0]

        # resources used
        self.resources_used = {}
        if 'resources_used' in pbsjobs_dict:
            self.resources_used['mem'] = Memory(pbsjobs_dict['resources_used']['mem'][0])
            self.resources_used['vmem'] = Memory(pbsjobs_dict['resources_used']['vmem'][0])
            self.resources_used['cput'] = pbstimestr_to_timedelta(pbsjobs_dict['resources_used']['cput'][0])
            self.resources_used['walltime'] = pbstimestr_to_timedelta(pbsjobs_dict['resources_used']['walltime'][0])

        if 'session_id' in pbsjobs_dict:
            self.session_id = int(pbsjobs_dict['session_id'][0])
        else:
            self.session_id = None

        # remaining walltime
        self.walltime_remaining = 0
        if 'Walltime' in pbsjobs_dict:
            self.walltime_remaining = datetime.timedelta(seconds=int(pbsjobs_dict['Walltime']['Remaining'][0]))

        ###
        ### These properties are available only to admin user:
        ###
        if 'substate' in pbsjobs_dict:
            self.substate = int(pbsjobs_dict['substate'][0])

        if 'Variable_List' in pbsjobs_dict:
            self.variable_list = pbsjobs_dict['Variable_List']
        else:
            self.variable_list = None

        if 'euser' in pbsjobs_dict:
            self.euser = pbsjobs_dict['euser'][0]
        else:
            self.euser = None

        if 'egroup' in pbsjobs_dict:
            self.egroup = pbsjobs_dict['egroup'][0]
        else:
            self.egroup = None

        if 'hashname' in pbsjobs_dict:
            self.hashname = pbsjobs_dict['hashname'][0]
        else:
            self.hashname = None

        if 'queue_rank' in pbsjobs_dict:
            self.queue_rank = int(pbsjobs_dict['queue_rank'][0])
        else:
            self.queue_rank = None

        if 'queue_type' in pbsjobs_dict:
            self.queue_type = pbsjobs_dict['queue_type'][0]
        else:
            self.queue_type = None

        ### End admin properties

        self.etime = datetime.datetime.fromtimestamp(int(pbsjobs_dict['etime'][0]))

        if 'exit_status' in pbsjobs_dict:
            self.exit_status = int(pbsjobs_dict['exit_status'][0])
        else:
            self.exit_status = None

        self.submit_args = pbsjobs_dict['submit_args'][0]
        
        if 'start_time' in pbsjobs_dict:
            self.start_time = datetime.datetime.fromtimestamp(int(pbsjobs_dict['start_time'][0]))
        else:
            self.start_time = None

        if 'start_count' in pbsjobs_dict:
            self.start_count = int(pbsjobs_dict['start_count'][0])
        else:
            self.start_count = None

        if 'fault_tolerant' in pbsjobs_dict:
            if pbsjobs_dict['fault_tolerant'][0] == 'True':
                self.fault_tolerant = True
            else:
                self.fault_tolerant = False
        else:
            self.fault_tolerant = None

        if 'submit_host' in pbsjobs_dict:
            self.submit_host = pbsjobs_dict['submit_host'][0]
        else:
            self.submit_host = None

        # 'x' is usually the nodeset spec
        if 'x' in pbsjobs_dict:
            self.extra = pbsjobs_dict['x'][0]
        else:
            self.extra = None


    def __count_ncpus(self):
        ncpus = 0
        ppn_pat = re.compile('^ppn=\d+$')
        node_req = self.resource_list['nodes'][0].split(':')
        for req in node_req:
            if ppn_pat.match(req):
                ncpus = int(req.split('=')[1]) * self.resource_list['nodect']

        if ncpus == 0:
            #nodepat = re.compile('^bcg?\d{2}bl{2}$')
            if self.state == 'R':
                ncpus = len(self.exec_host)
            else:
                nodereq = self.resource_list['nodes'][0].split('+')
                ncpus = len(nodereq)
        return ncpus


    def __list_unique_hosts(self):
        uniq_hosts = set()
        if self.exec_host:
            for h in self.exec_host:
                uniq_hosts.add(h.split('/')[0])
        return uniq_hosts


    def __str__(self):
        return str(self.__dict__)
        

if __name__ == '__main__':
    pq = PBSQuery()
    jobs = {}
    for k,v in pq.getjobs().iteritems():
        #print type(dict(v))
        #print dict(v)
        jobs[k] = Job(id=k, pbsjobs_dict=dict(v))

    for k,v in jobs.iteritems():
        print k, ': ', v, '\n'
        #print v.id, ': ', v.job_state


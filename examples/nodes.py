#!/usr/bin/env python

# Author: G. Lopez <lopemg6 . wfu.edu>

# this is just a script to print out some information about what is going on with
# the nodes in the cluster.  written by g. lopez.

import os
import sys
import getopt
import re

from optparse import OptionParser

# these are for the colors used to print the output.  Go to the bottom of this
# script to change the values
#
# Attribute codes:
# 00=none 01=bold 04=underscore 05=blink 07=reverse 08=concealed
# Text color codes:
# 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white
# Background color codes:
# 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white
#
# example: underscored red with yellow background --> 4;31;33
#
RED = '\033[0;31m'
BOLDRED = '\033[1;31m'

GREEN = '\033[0;32m'
BOLDGREEN = '\033[1;32m'

YELLOW = '\033[0;33m'
BOLDYELLOW = '\033[1;33m'

BLUE = '\033[0;34m'
BOLDBLUE = '\033[1;34m'

PURPLE = '\033[0;35m'
BOLDPURPLE = '\033[1;35m'

CYAN = '\033[0;36m'
BOLDCYAN = '\033[1;36m'

WHITE = '\033[0;37m'
BOLDWHITE = '\033[1;37m'

BLACK = '\033[0;30m'
BOLDBLACK = '\033[1;30m'

DEF = '\033[0;00m'

END = '\033[0m'

# Here you can set the defaults for the command line options if you find that
# you use a certain combination most of the time.  see usage message below for
# a reminder of what does what
#
# these are just defaults, they are overridden by the command line options

want_mem        = -1    # get any value for memory
want_procs      = -1    # get any number of procs
want_net        = "all" # get all kinds of networking
want_clan       = "all" # get all clans
want_job        = ".*"  # get all job descriptions
want_free       = False # don't print non-matching, free nodes
want_all        = False # don't print offline nodes

pbsnodes_command = "pbsnodes"
qstat_command = "qstat -f"

# define some functions

def print_usage():
    """Print usage instructions"""

    print"""\
usage: nodes.py [options]
show cluster usage information like which nodes are free.  if [options] are
given that specify conditions, only those nodes matching those conditions
will be shown by default (unless -a, --all is also specified).  the default
is to print all nodes that are online.

    -h, --help                  print this usage message
    -m N, --mem=N               want nodes with at least N mb of total mem
    -p N, --procs=N             want nodes with at least N procs free
    -n network, --net=network   want nodes with "network" type interconnect
    -c name, --clan=name        want nodes belonging to clan(s) "name"
                                (note that this can be a comma-delimited list)
    -a, --all                   print all nodes
    -f, --free                  print all free or matching nodes
    -j [string], --job=string   search for "string" in job description

    (not implemented yet)
    -p [string], --print=[string]   which info to print (see below)

    one may also specify which fields of information to print about the nodes.
    note that one can use options above to filter, yet not print that info, or
    print info that was not filtered.

    [string] is specified by a single letters, delimited by commas
    a = print arch info
    m = print mem info
    p = print proc info
    n = print net info
    c = print clan info
    e = print everything (default)
    j = print job info


specifying any of the above options will cause nodes matching those
criteria to be printed in (color)
    """
    sys.exit(0)

# set up the "classes" (glorfied structs) that will be used

class node:
    def __init__(self, name):
        self.name = name
    def add_state(self, state):
        self.state = state
    def add_clan(self, clan):
        self.clan = clan
    def add_net(self, network):
        self.net = network
    def add_mem(self, memory):
        self.mem = memory
    def add_fprocs(self, nprocs):
        self.fprocs = nprocs
    def add_tprocs(self, nprocs):
        self.tprocs = nprocs
    #def add_arch(self, arch):
    #    self.arch = arch
    online = True

class job:
    def __init__(self, id):
        self.id = id
        self.nodes = -1
    def add_nodes(self, node):
        self.nodes = node
    def add_name(self, name):
        self.name = name
    def add_owner(self, owner):
        self.owner = owner
    def add_nprocs(self, nprocs):
        self.nprocs = nprocs


# process the command line options

try:
    optlist, args  = getopt.getopt(sys.argv[1:], 'hm:p:n:c:ax:j:f', \
        ['help', 'mem=', 'procs=', 'net=', 'clan=', 'all', 'job=', 'free'])

except getopt.GetoptError, errstring: # invalid option, or no required arg, etc.
    print errstring.msg
    sys.exit(2) # '2' generally used for command line syntax errors, '1' for all else

for opt, arg in optlist:
    if opt in ('-h', '--help'):
        print_usage()
    elif opt in ('-m', '--mem'):
        want_mem = int(arg)
    elif opt in ('-p', '--procs'):
        want_procs = int(arg)
    elif opt in ('-n', '--net'):
        want_net = arg
    elif opt in ('-c', '--clan'):
        want_clan = arg
    elif opt in ('-a', '--all'):
        want_all = True
    elif opt in ('-j', '--job'):
        want_job = arg
    elif opt in ('-f', '--free'):
        want_free = True

hosts = []
jobs = []

# compile the regexes that we will need
hostname    = re.compile("deac\d+|bc\d+bl\d+")
gig         = re.compile('mem(\d+)gb')
meg         = re.compile('mem(\d+)mb')
#arch        = re.compile('arch=(\w+|\w+_\w+),')

output = os.popen(pbsnodes_command,'r',-1)

for line in output:

    if hostname.match(line):
        x = node(line.strip())
        hosts.append(x) # add this guy to our list of hosts

        # now get the info about the host (status string and total number of procs)
        x.add_state(output.next().split('=')[-1].strip())
        if re.search(r'down|offline',x.state):
            x.online = False
            #continue

        x.add_tprocs(int(output.next().split('=')[-1].strip()))

        tmp = output.next().split('=')[-1].strip().split(',')

        # get info about best networking on the host
        if tmp.count("infiniband") > 0:
            x.add_net("infiniband")
        elif tmp.count("infiniband03"):
            x.add_net("infiniband03")
        elif tmp.count("infiniband02"):
            x.add_net("infiniband02")
        elif tmp.count("infiniband01"):
            x.add_net("infiniband01")
        elif tmp.count("myrinet"):
            x.add_net("myrinet")
        elif tmp.count("ethernet"):
            x.add_net("ethernet")

        # get info about amount of memory
        for i in tmp:
            m = gig.match(i)
            if m:
                x.add_mem(int(m.group(1))*1000)
            m = meg.match(i)
            if m:
                x.add_mem(int(m.group(1)))

        # get clan name
        for i in tmp:
            if re.match(r'clan\d+',i):
                x.add_clan(i)

        tmp = output.next() # chomp the 'ntype' line

        # look for number of used processors
        tmp = output.next()
        if re.match(r'\s*jobs',tmp):
            num = len(tmp.split('=')[-1].strip().split(','))
            x.add_fprocs(num)
            tmp = output.next()
        else:
            x.add_fprocs(0)

        # look for architecture type
        #if re.match(r'\s*status',tmp):
        #    m = arch.search(tmp)
        #    if m:
        #        x.add_arch(m.group(1))

output.close()
# end pbsnodes for

# get information about jobs from qstat

output = os.popen(qstat_command,'r',-1)

jobidre     = re.compile(r'Job\ Id:\ (\d+)')
jobnamere   = re.compile(r'\s*Job_Name\ =\ (\S+)')
jobownre    = re.compile(r'\s*Job_Owner\ =\ (\S+)')
jobhosts    = re.compile(r'\s*exec_host\ =\ (\S+)')

for line in output:

    m = jobidre.match(line)
    if m:
        x = job(m.group(1))
        jobs.append(x)

        m = jobnamere.match(output.next())
        if m:
            x.add_name(m.group(1))

        m = jobownre.match(output.next())
        if m:
            x.add_owner(m.group(1).split('@')[0])


    m = jobhosts.match(line)
    if m:
        tmp_line1 = line
        tmp_line2 = ""
        while not re.match(r'\s*group_list',tmp_line1):
            tmp_line2 = "".join((tmp_line2,tmp_line1.strip()))
            tmp_line1 = output.next()

        hns = tmp_line2.split('=')[-1].strip().split('+')
        x.add_nodes(hns)
        x.add_nprocs(len(hns))

output.close()


# time to print stuff out

print "key: %sgreen = match, %snormal = free (but not match), %sred = not available%s" % (GREEN, DEF, RED, END)
print "%s%s|%s|%s|%s|%s|%s|%s%s" % (DEF, "name".center(10), "clan".center(8), \
        " procs ", "mem".center(7), "net".center(5), "state".center(8), " job desc. (id, owner, name, loc/tot #procs)", END)
print "----------------------------------------------------------------------------------------------------------------------"
prev_clan = hosts[0].clan
for y in hosts:
    if not y.online:
        if want_all:
            print "%s%s| is down/offline !!" % (RED, y.name.center(10))

    else:
        # get stuff ready to print out job info
        job_desc = "no jobs"
        for n in jobs:
            if n.nodes != -1:
                for j in n.nodes:
                    if re.search(y.name, j):
                        local_nprocs = 0
                        for k in n.nodes:
                            if re.search(y.name, k):
                                local_nprocs = local_nprocs+1
                        job_desc = "id=%s, o=%s, n=%s, np=%d/%d" % (n.id, n.owner, n.name[-10:], local_nprocs, n.nprocs)

        # look for nodes that match user's criteria
        if (y.clan == want_clan or want_clan == "all") \
            and (y.net  == want_net  or want_net  == "all") \
            and (y.mem  >= want_mem) \
            and ((y.tprocs - y.fprocs) >= want_procs) \
            and (y.online) \
            and (re.search(want_job,job_desc)):

        #and (re.search(want_job,job_desc)):

            # to print out spaces between clans
            if not y.clan == prev_clan:
                print ""
                prev_clan = y.clan

            print "%s%s|%s|  %d/%d  |%s|%s|%s| %s%s" % (GREEN, y.name.center(10), y.clan.center(8), \
                y.fprocs, y.tprocs, str(y.mem).center(7), y.net[:3].center(5), y.state[:6].center(8), job_desc, END)

        # if they also wanted "free" nodes
        elif want_free:
            if y.state == "free":

                # to print out spaces between clans
                if not y.clan == prev_clan:
                    print ""
                    prev_clan = y.clan

                print "%s%s|%s|%s|  %d/%d  |%s|%s| %s%s" % (DEF, y.name.center(10), y.clan.center(8), \
                    y.fprocs, y.tprocs, str(y.mem).center(7), y.net[:3].center(5), y.state[:6].center(8), job_desc, END)


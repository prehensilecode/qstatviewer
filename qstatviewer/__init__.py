#!/usr/bin/env python
"""
Encapsulates information about jobs in a TORQUE queue.
"""

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import sys, os, re, string, copy
import shlex
import subprocess
import pickle

from PBSQuery import PBSQuery

from StringIO import StringIO


from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory, timedeltastr

from qstatviewer.Node import Node
from qstatviewer.Job import Job
from qstatviewer.QstatViewer import QstatViewer


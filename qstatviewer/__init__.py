#!/usr/bin/env python
"""
Encapsulates information about jobs in a TORQUE queue.
"""

# Author: David Chin <dwchin@acm.org>
# $Id: __init__.py 479 2013-02-20 16:27:37Z chindw $

# qstatviewer by David Chin is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

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


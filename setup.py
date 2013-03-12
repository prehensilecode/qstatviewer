#!/usr/bin/env python

# Author: David Chin <dwchin@acm.org>
# $Id: setup.py 488 2013-03-06 20:41:05Z chindw $

"""Build/install script for qstatviewer. 
See INSTALL for installation instructions.
"""

from distutils.core import setup

setup(name = 'qstatviewer',
      version = '0.8.5',
      packages = ['qstatviewer'],
      scripts = ['scripts/viewnodes', 'scripts/viewjobs', 'scripts/userjobs', 'scripts/users_on_node', 'scripts/jobinfo_node'],
      license = 'GPL',
      author = 'David Chin',
      author_email = 'dwchin@acm.org',
      maintainer = 'David Chin',
      maintainer_email = 'dwchin@acm.org',
      description = 'Encapsulates information about TORQUE jobs',
      url = 'http://users.wfu.edu/chindw/', 
      download_url = 'http://users.wfu.edu/chindw/qstatviewer',
      )


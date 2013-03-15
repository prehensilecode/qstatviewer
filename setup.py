#!/usr/bin/env python

# Author: David Chin <dwchin . acm.org>

"""Build/install script for qstatviewer. 
See INSTALL for installation instructions.
"""

from distutils.core import setup

# When building RPMs, the "license" string may have to be changed to 'GPL'

setup(name = 'qstatviewer',
      version = '0.8.6',
      packages = ['qstatviewer'],
      scripts = ['scripts/viewnodes', 'scripts/viewjobs', 'scripts/userjobs', 'scripts/users_on_node', 'scripts/jobinfo_node'],
      license = 'CC-BY-SA 3.0',
      author = 'David Chin',
      author_email = 'dwchin@acm.org',
      maintainer = 'David Chin',
      maintainer_email = 'dwchin@acm.org',
      description = 'Encapsulates information about TORQUE jobs',
      url = 'https://github.com/prehensilecode/qstatviewer', 
      download_url = 'https://github.com/prehensilecode/qstatviewer',
      )


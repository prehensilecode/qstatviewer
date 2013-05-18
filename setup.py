#!/usr/bin/env python

# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

"""Build/install script for qstatviewer. 
See INSTALL for installation instructions.
"""

from distutils.core import setup

# When building RPMs, the "license" string may have to be changed to 'GPL'

setup(name = 'qstatviewer',
      version = '0.9.23',
      packages = ['qstatviewer'],
      scripts = ['scripts/viewnodes', 'scripts/viewjobs', 'scripts/userjobs', 
        'scripts/users_on_node', 'scripts/jobinfo_node', 'scripts/jobdetail',
        'scripts/nodedetail'],
      license = 'Copyright 2013 Wake Forest University',
      author = 'David Chin',
      author_email = 'dwchin@acm.org',
      maintainer = 'David Chin',
      maintainer_email = 'dwchin@acm.org',
      description = 'Encapsulates information about TORQUE jobs',
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Topic :: System :: Distributed Computing',
      ],
      url = 'https://github.com/prehensilecode/qstatviewer', 
      download_url = 'https://github.com/prehensilecode/qstatviewer',
      )


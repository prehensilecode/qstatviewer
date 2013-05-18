#!/usr/bin/env python
import sys
import os
import re

from PBSQuery import PBSQuery

def main():
    pq = PBSQuery()
    queuedict = pq.getqueues()
    print queuedict
    for queuename, queue in sorted(queuedict.iteritems()):
        print queuename
        for k, v in queue.iteritems():
            print k, v
        print

if __name__ == '__main__':
    main()


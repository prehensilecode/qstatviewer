#!/usr/bin/env python
import sys
import os
import re

from PBSQuery import PBSQuery

def main():
    pq = PBSQuery()
    print 'Server:',pq.server
    serverinfo = pq.get_serverinfo()
    for k, v in sorted(serverinfo.iteritems()):
        print k 
        for i, j in sorted(v.iteritems()):
            print i, j

if __name__ == '__main__':
    main()


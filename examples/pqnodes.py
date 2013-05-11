#!/usr/bin/env python
import sys
import os
import re

from PBSQuery import PBSQuery

def main():
    pq = PBSQuery()
    nodedict = pq.getnodes()
    for nodename, node in sorted(nodedict.iteritems()):
        print nodename
        for k, v in node.iteritems():
            print k, v

if __name__ == '__main__':
    main()


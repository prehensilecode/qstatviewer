#!/usr/bin/env python

import sys
import os
import re

from PBSQuery import PBSQuery

def main():
    pq = PBSQuery()
    nodes = pq.getnodes()
    for k,v in sorted(nodes.iteritems()):
        print k, v['state']
    

if __name__ == '__main__':
    main()


#!/usr/bin/env python
# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import sys, os, re

from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory

class Memory:
    """
    Represents amount of memory
    """
    def __init__(self, memstr="", memamt={}):
        self.__KILO = 1024.
        self.__MEGA = 1048576.
        self.__kiB = 'kiB'
        self.__MiB = 'MiB'
        self.__GiB = 'GiB'

        if memstr:
            self.__mem = convert_memory(memstr, 'kb')
        elif memamt:
            self.__mem = memamt

        self.qty = self.__mem['qty']
        self.units = self.__mem['units']

    def in_MiB(self):
        if self.units == self.__kiB:
            qty = self.qty / self.__KILO
        elif self.units == self.__GiB:
            qty = self.qty * self.__KILO

        units = self.__MiB
        mem = {'qty': qty, 'units': units}
        return Memory(memamt=mem)

    def in_GiB(self):
        if self.units == self.__kiB:
            qty = self.qty / self.__MEGA
        elif self.units == self.__MiB:
            qty = self.qty / self.__KILO

        units = self.__GiB
        mem = {'qty': qty, 'units': units}
        return Memory(memamt=mem)

    def __str__(self):
        fmtstr = "{qty:4.2f} {units:3.3}"
        return fmtstr.format(qty=self.qty, units=self.units)
        

if __name__ == '__main__':
    mem = Memory('1274127387kb')
    print(mem)
    print(mem.in_GiB())
    print(mem.in_MiB())
    
    print("")

    mem = Memory('1536mb')
    print(mem)
    print(mem.in_GiB())
    print(mem.in_MiB())


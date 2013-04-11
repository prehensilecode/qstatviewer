#!/usr/bin/env python
# Author: David Chin <dwchin@acm.org>
# Copyright 2013 Wake Forest University

import sys, os, re
import copy

from qstatviewer.config import __version__, jobstate_dict, nodestate_dict, convert_memory

class Memory:
    """
    Represents amount of memory
    """
    def __init__(self, mem):
        self.__KILO = 1024.
        self.__MEGA = 1048576.
        self.__kiB = 'kiB'
        self.__MiB = 'MiB'
        self.__GiB = 'GiB'

        if type(mem) == str:
            self.__mem = convert_memory(mem, 'kb')
        elif type(mem) == dict:
            self.__mem = mem
        elif type(mem) == int or type(mem) == float:
            # assume kiB
            memstr = ''.join([str(mem), 'kb'])
            self.__mem = {'qty': mem, 'units': self.__kiB}
        else:
            raise Exception

        #if memstr:
        #    self.__mem = convert_memory(memstr, 'kb')
        #elif memamt:
        #    self.__mem = memamt

        self.qty = self.__mem['qty']
        self.units = self.__mem['units']

        self.__to_kiB()



    def in_MiB(self):
        qty = 0.
        if self.units == self.__kiB:
            qty = self.qty / self.__KILO
        elif self.units == self.__GiB:
            qty = self.qty * self.__KILO

        units = self.__MiB
        mem = {'qty': qty, 'units': units}
        if mem['qty'] < 1:
            formatstr = "{qty:.2e} {units:3.3}"
        else:
            formatstr = "{qty:.2f} {units:3.3}"
        return formatstr.format(qty=mem['qty'], units = mem['units'])

    def in_GiB(self):
        qty = 0.
        if self.units == self.__kiB:
            qty = self.qty / self.__MEGA
        elif self.units == self.__MiB:
            qty = self.qty / self.__KILO

        units = self.__GiB
        mem = {'qty': qty, 'units': units}
        if mem['qty'] < 1:
            formatstr = "{qty:.2e} {units:3.3}"
        else:
            formatstr = "{qty:.2f} {units:3.3}"
        return formatstr.format(qty=mem['qty'], units = mem['units'])


    def copy(self):
        return copy.deepcopy(self)


    def __to_kiB(self):
        """convert to kiB"""

        if self.__mem['units'] != self.__kiB:
            if self.__mem['units'] == self.__MiB:
                self.__mem['qty'] *= self.__KILO
            elif self.__mem['units'] == self.__GiB:
                self.__mem['qty'] *= self.__MEGA

            self.__mem['units'] = self.__kiB

            self.qty = self.__mem['qty']
            self.units = self.__mem['units']


    def __cmp__(self, other):
        # make sure
        pass


    def __str__(self):
        fmtstr = "{qty:.2f} {units:3.3}"
        return fmtstr.format(qty=self.qty, units=self.units)
        

if __name__ == '__main__':
    mem = Memory('1274127387kb')
    print(mem)
    print(mem.qty)
    print(mem.units)
    print(mem.in_GiB())
    print(mem.in_MiB())
    
    print("")

    mem = Memory('1536mb')
    print(mem)
    print(mem.qty)
    print(mem.units)
    print(mem.in_GiB())
    print(mem.in_MiB())

    print("")

    mem2 = mem.copy()
    print(mem2)
    print(mem2.qty)
    print(mem2.units)
    print(mem2.in_GiB())
    print(mem2.in_MiB())

    print("")

    foo = {'qty': 13.235, 'units': 'GiB'}
    mem3 = Memory(foo)
    print(mem3)
    print(mem3.qty)
    print(mem3.units)
    print(mem3.in_GiB())
    print(mem3.in_MiB())

    print("")

    mem4 = Memory(25.2)
    print(mem4)
    print(mem4.qty)
    print(mem4.units)
    print(mem4.in_GiB())
    print(mem4.in_MiB())

    print("")

    mem4 = Memory(900.7)
    print(mem4)
    print(mem4.qty)
    print(mem4.units)
    print(mem4.in_GiB())
    print(mem4.in_MiB())


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
    def __init__(self, mem=None):
        # Example inputs:
        # - '1024mb'
        # - {'qty': 4239.123, 'units': 'GiB'}
        # - 123
        # - 123.456
        self.__KILO = 1024.
        self.__MEGA = 1048576.
        self.__kiB = 'kiB'
        self.__MiB = 'MiB'
        self.__GiB = 'GiB'

        if mem:
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
        else:
            self.__mem = {'qty': 0., 'units': self.__kiB}

        self.qty = self.__mem['qty']
        self.units = self.__mem['units']

        self.__to_kiB()


    def in_MiB(self):
        """Returns float of qty in MiB"""
        qty = 0.
        if self.units == self.__kiB:
            qty = self.qty / self.__KILO
        elif self.units == self.__GiB:
            qty = self.qty * self.__KILO

        return qty


    def in_GiB(self):
        """Returns float of qty in GiB"""
        qty = 0.
        if self.units == self.__kiB:
            qty = self.qty / self.__MEGA
        elif self.units == self.__MiB:
            qty = self.qty / self.__KILO

        return qty


    def str_in_MiB(self):
        qty = self.in_MiB()
        units = self.__MiB
        formatstr = ""
        if qty < 1:
            formatstr = "{qty:.2e} {units:3.3}"
        else:
            formatstr = "{qty:.2f} {units:3.3}"

        return formatstr.format(qty=qty, units=units)


    def str_in_GiB(self):
        qty = self.in_GiB()
        units = self.__GiB
        if qty < 1:
            formatstr = "{qty:.2e} {units:3.3}"
        else:
            formatstr = "{qty:.2f} {units:3.3}"
        return formatstr.format(qty=qty, units=units)


    def copy(self):
        return copy.deepcopy(self)


    def pretty_print(self):
        """Select appropriate units based on quantity"""
        qty = 0.
        units = ''
        if self.__mem['qty'] < 1:
            qty = self.__mem['qty'] * self.__KILO
            units = 'B'
        elif self.in_MiB() < 1:
            qty = self.__mem['qty']
            units = self.__mem['units']
        elif self.in_GiB() < 1:
            qty = self.in_MiB()
            units = self.__MiB
        else:
            qty = self.in_GiB()
            units = self.__GiB

        formatstr = ""
        if qty < 1:
            formatstr = "{qty:.2e} {units:<}"
        else:
            formatstr = "{qty:.2f} {units:<}"
        return formatstr.format(qty=qty, units=units)
        

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
        return (self.__mem['qty'] - other.__mem['qty'])

    
    def __add__(self, other):
        return Memory(self.__mem['qty'] + other.__mem['qty'])


    def __sub__(self, other):
        return Memory(self.__mem['qty'] - other.__mem['qty'])

    
    def __repr__(self):
        formatstr = "{qty:.2f} {units:3.3}"
        if self.qty < 1:
            formatstr = "{qty:.2e} {units:3.3}"
        else:
            formatstr = "{qty:.2f} {units:3.3}"
        return formatstr.format(qty=self.qty, units=self.units)


    def __str__(self):
        return self.__repr__()
        

if __name__ == '__main__':
    print("TEST 0")
    memstr = "1234MiB"
    print("memstr = ", memstr)
    mem = Memory(memstr)
    print("mem = ", mem)
    memstr = "1234kiB"
    print("memstr = ", memstr)
    mem = Memory(memstr)
    print("mem = ", mem)
    
    print("")

    print("TEST 1")
    mem = Memory('1274127387kb')
    print(mem)
    print(mem.qty)
    print(mem.units)
    print(mem.in_GiB())
    print(mem.str_in_GiB())
    print(mem.in_MiB())
    print(mem.str_in_MiB())
    print(mem.pretty_print())
    
    print("")

    print("TEST 2")
    mem = Memory('1536mb')
    print(mem)
    print(mem.qty)
    print(mem.units)
    print(mem.in_GiB())
    print(mem.str_in_GiB())
    print(mem.in_MiB())
    print(mem.str_in_MiB())
    print(mem.pretty_print())

    print("")

    print("TEST 3")
    mem = Memory()
    print(mem)
    print(mem.qty)
    print(mem.units)
    print(mem.in_GiB())
    print(mem.str_in_GiB())
    print(mem.in_MiB())
    print(mem.str_in_MiB())
    print(mem.pretty_print())

    print("")

    print("TEST 4")
    mem2 = mem.copy()
    print(mem2)
    print(mem2.qty)
    print(mem2.units)
    print(mem2.in_GiB())
    print(mem2.str_in_GiB())
    print(mem2.in_MiB())
    print(mem2.str_in_MiB())
    print(mem2.pretty_print())

    print("")

    print("TEST 5")
    foo = {'qty': 13.235, 'units': 'GiB'}
    mem3 = Memory(foo)
    print(mem3)
    print(mem3.qty)
    print(mem3.units)
    print(mem3.in_GiB())
    print(mem3.str_in_GiB())
    print(mem3.in_MiB())
    print(mem3.str_in_MiB())
    print(mem3.pretty_print())

    print("")

    print("TEST 6")
    mem4 = Memory(25.2)
    print(mem4)
    print(mem4.qty)
    print(mem4.units)
    print(mem4.in_GiB())
    print(mem4.str_in_GiB())
    print(mem4.in_MiB())
    print(mem4.str_in_MiB())
    print(mem4.pretty_print())

    print("")

    print("TEST 7")
    mem5 = Memory(900.7)
    print(mem5)
    print(mem5.qty)
    print(mem5.units)
    print(mem5.in_GiB())
    print(mem5.str_in_GiB())
    print(mem5.in_MiB())
    print(mem5.str_in_MiB())
    print(mem5.pretty_print())

    print("")

    print("TEST 8")
    print("mem3 = {0}".format(mem3))
    print("mem4 = {0}".format(mem4))
    print("mem5 = {0}".format(mem5))

    print("mem3 < mem4 = {0}".format((mem3 < mem4)))
    print("mem4 < mem3 = {0}".format((mem4 < mem3)))
    print("mem4 < mem5 = {0}".format((mem4 < mem5)))
    print("mem5 < mem4 = {0}".format((mem5 < mem4)))
    print("mem5 == mem5 = {0}".format((mem5 == mem5)))
    

    print("mem3 + mem4 = {0}".format(mem3 + mem4))
    print("mem4 - mem3 = {0}".format(mem4 - mem3))


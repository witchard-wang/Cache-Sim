# File: set.py
# Authors: Richard Wang   - Elijah Hawkins
# Date: 04/30/2020
# Section: 511            - 509
# E-mail: r.wang@tamu.edu - hawkeli@tamu.edu
# Description:
# This file contains the class for the set 
# it is an abstract module of sets for the cache

class set:
    def __init__(self, block):
        self.tag = 0
        self.uses = 0
        self.valid = 0
        self.dirty = 0
        self.data = ["00"] * block

    def setData(self, index, val):
        self.data[index] = val
    #set block of data in cache line 
    def setBlock(self, nlist):
        for i,elem in enumerate(nlist):
            self.data[i] = elem

    #gets a string of all data stored in cache line
    def getData(self):
        hexTag = hex(self.tag)[2:].zfill(2).upper()
        line = ""
        for val in self.data:
            line += val + " "
        line += "\n"
        return line

    #prints cache line information
    def printLine(self):
        hexTag = hex(self.tag)[2:].zfill(2).upper()
        print(self.valid, end= " ")
        print(self.dirty, end= " ")
        print(hexTag, end = " ")
        for val in self.data:
            print(val, end= " ")
        print()
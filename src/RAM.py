# File: RAM.py
# Authors: Richard Wang   - Elijah Hawkins
# Date: 04/30/2020
# Section: 511            - 509
# E-mail: r.wang@tamu.edu - hawkeli@tamu.edu
# Description:
# This file is used to store the RAM data from an input text file

class RAM:
    def __init__(self):
        self.ram = []
        self.ramCnt = 0

    def getBlock(self, idx, B):
        count = 0
        block = []
        for val in ram[idx:idx+B]:
            block.append(val)
        return block


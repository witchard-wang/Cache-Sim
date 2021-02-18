# File: RAM.py
# Authors: Richard Wang   - Elijah Hawkins
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


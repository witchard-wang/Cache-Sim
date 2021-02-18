#Authors: Richard Wang - Elijah Hawkins
# Authors: Richard Wang   - Elijah Hawkins
# Date: 04/30/2020
# Section: 511            - 509
# E-mail: r.wang@tamu.edu - hawkeli@tamu.edu
#cache simulator 
#file: cachesimulator.py

#This file contains the main method and methods with user inputs
#to configure cache

import sys
import cache
import RAM

class Simulator(object):
    #initialize simulator
    def __init__(self):
        self.mem_RAM = RAM.RAM()
        self.cacheSim = cache.cache(1,1,1,0,0,0,1, self.mem_RAM)

    #Input file data into ram class
    def initialize(self, fname):
        print("***Welcome to the cache simulator***")
        print("initialize the RAM:")
        with open(fname, 'r') as rm:
            #loop through input file and map data to ram
            for line in rm.readlines():
                word = line.strip()
                if(word != ""):
                    self.mem_RAM.ram.append(word)
                    self.mem_RAM.ramCnt += 1
        beg = hex(0).zfill(2)
        end = hex(self.mem_RAM.ramCnt-1).zfill(2)
        title = "init-ram " + beg + " " + end
        print(title)
        print("ram successfully initialized!")

    #configure cache
    def configure(self):
        # global cacheSim
        rep = 0
        hit = 0
        miss = 0
        print("configure the cache: ")
        S = int(input("cache size: "))
        while(not (S >= 8 and S <= 256)):
            S = int(input("Not a valid input (enter integer between 8 and 256): "))
        B = int(input("data block size: "))
        E = int(input("associativity: "))
        while not((E != 1) or (E != 2) or (E != 4)):
            E = int(input("Not a valid input (enter 1,2, or 4): "))

        rep = int(input("replacement policy: "))
        hit = int(input("write hit policy: "))
        miss = int(input("write miss policy: "))
        while not(rep != 1 or rep != 2):
            rep = int(input("Not a valid input (enter 1 or 2): "))
        while not(hit != 1 or hit != 2):
            hit = int(input("Not a valid input (enter 1 or 2): "))
        while not(miss != 1 or miss != 2):
            miss = int(input("Not a valid input (enter 1 or 2): "))

        self.cacheSim = cache.cache(S, E, B, rep, hit, miss, self.mem_RAM.ramCnt, self.mem_RAM.ram)
        print("cache successfuly configured: ")

    #dumps contents of memory into ram.txt
    def memDump(self):
        with open("ram.txt", 'w') as mdump:
            for key in self.mem_RAM.ram:
                line = key + "\n"
                mdump.write(line)

    #view memory through command line
    def memView(self):
        count = 0
        print("memory-size:" + str(self.mem_RAM.ramCnt))
        print("Address:Data")
        for data in self.mem_RAM.ram:
            if(count % 8 == 0):
                print("0x" + hex(count)[2:].zfill(2).upper(), end=":")

            if(count % 8 != 7):
                print(data, end=" ")
            else:
                print(data)
            count += 1

    def printmenu(self):
        while(True):
            print("*** Cache simulator menu ***")
            print("type one command:")
            print("1. cache-read")
            print("2. cache-write")
            print("3. cache-flush")
            print("4. cache-view")
            print("5. memory-view")
            print("6. cache-dump")
            print("7. memory-dump")
            print("8. quit")
            print("****************************")
            inp = input().split(" ")
            if(inp[0] == "cache-read"):
                read = inp[1]
                self.cacheSim.read(read)
                self.mem_RAM.ram = self.cacheSim.mem
            elif(inp[0] == "cache-write"):
                write = inp[1]
                data = inp[2]
                self.cacheSim.write(write, data)
                self.mem_RAM.ram = self.cacheSim.mem
            elif(inp[0] == "cache-flush"):
                self.cacheSim.flush()
                self.mem_RAM.ram = self.cacheSim.mem
            elif(inp[0] == "cache-view"):
                self.cacheSim.cView()
            elif(inp[0] == "memory-view"):
                self.memView()
            elif(inp[0] == "cache-dump"):
                self.cacheSim.cDump()
            elif(inp[0] == "memory-dump"):
                self.memDump()
            elif(inp[0] == "quit"):
                break
            else:
                inp = input("Not a valid input")

def main(argv):
    file = argv[1]
    sim = Simulator()
    sim.initialize(file)
    sim.configure()
    sim.printmenu()


    # sim.memdump()
    # sim.memView()
    # sim.cacheSim.cView()
    
    
    
    

if __name__ == "__main__":
    main(sys.argv[0:])
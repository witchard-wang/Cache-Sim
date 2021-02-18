# File: cache.py
# Authors: Richard Wang   - Elijah Hawkins
# Date: 04/30/2020
# Section: 511            - 509
# E-mail: r.wang@tamu.edu - hawkeli@tamu.edu

#contains the cache module including function definitions
#for different cache methods such as read, write, cache view and cache dump
#as well as helper methods for the cache methods

from math import log, ceil
import random
import set
import RAM

class cache(object):
    def __init__(self, size, E, B, rep, hit, miss, memsize, ram):
        #cache info
        self.size = size
        mul = B*E
        if(mul == 0):
            mul = 1
        self.Sets = size // mul
        self.E = E
        self.B = B
        self.numHits = 0
        self.numMiss = 0

        #policies
        self.rep = rep #replacement policy
        self.hit = hit #write hit policy
        self.miss = miss #write miss policy

        #cache address bits size
        self.membit = ceil(log(memsize, 2))
        self.setbit = ceil(log(self.Sets, 2))
        self.blockbit = ceil(log(B, 2))
        self.tagbit = self.membit - self.setbit - self.blockbit

        self.mem = ram
        #cache storage
        self.line = set.set(B) #set line
        self.storage = [[self.line for i in range(E)] for j in range(self.Sets)] #set storage
        
    # cache-read
    def read(self, data):
        hit = True
        evict = -1
        address = int(data, 0)
        binAdd = bin(address)[2:].zfill(self.membit)
        split = self.splitAddress(binAdd)
        blockb = split[2]
        setb = split[1]
        tagb = split[0]
        print("set:" + str(setb))
        print("tag:" + str(tagb))
        
        #check hit or miss
        val = 0
        count = 0
        linenum = -1
        linenum2 = -1
        for x in self.storage[setb]:
            #line already in cache (hit)
            if x.valid == 1 and tagb == x.tag:
                flag = True
                linenum = count
                break
            #line not found after looping through (miss)
            else:
                flag = False
            
            #check if there is a missing line in cache
            if x.valid == 1:
                val += 1
            #get missing line number
            elif linenum2 == -1:
                linenum2 = count
            count += 1
        
        dataVal = ""
        if flag == True:
            print("hit:yes")
            self.numHits += 1
            data = self.read_hit(setb, tagb, blockb, linenum, address)
            dataVal = self.convHex(self.storage[setb][linenum].data[blockb])
        else:
            print("hit:no")
            self.numMiss += 1
            evict = self.read_miss(setb, tagb, blockb, linenum2, val, address)
            dataVal = self.convHex(self.mem[address])
        print("eviction_line:" + str(evict))
        print("ram_address:" + str(data))
        print("data:" + dataVal)

    def read_hit(self, setb, tagb, blockb, linenum, address):
        line = self.storage[setb][linenum]
        line.uses += 1
        return -1

    #read miss - reads in line from RAM to cache 
    def read_miss(self, setb, tagb, blockb, linenum, val, address):
        evict = 0
        
        #evict invalid empty line first
        if val != self.E:
            evict = linenum
            
        else:
            #random replacement
            if self.rep == 1:
                evict = random.randint(0, self.E -1)
            
            #Least Recently used    
            else:
                least = self.storage[setb][0]
                count = 0
                for lines in self.storage[setb]:
                    if lines.uses < least.uses:
                        least = lines 
                        evict = count
                    count += 1
        #write dirty line to RAM
        self.write_dirty(self.storage[setb][evict], evict)

        #subtract uses from all lines
        for old in self.storage[setb]:
            old.uses -= 1
            
        #evict line from cache set
        line = set.set(self.B)
        count = 0
        # calc ram mem location
        tagbin = bin(tagb)[2:]
        setbin = bin(setb)[2:]
        total = (tagbin + setbin).ljust(self.membit, '0')
        add = int(total, 2)
        block = []
        for val in self.mem[add:add + self.B]:
            block.append(val)
        line.valid = 1
        line.tag = tagb
        line.uses = 1
        line.dirty = 0
        line.data = block
        self.storage[setb][evict] = line
        return evict

    # cache-write - writes data to address in RAM/Cache depending on policy
    def write(self, address, data):
        dirty = 0
        evict = -1
        data = data[2:]
        add = int(address, 0) #convert to decimal
        binAdd = bin(add)[2:].zfill(self.membit)
        split = self.splitAddress(binAdd)
        blockb = split[2]
        setb = split[1]
        tagb = split[0]
        if(split[1] == ""):
            setb = 0

        print("set:" + str(setb))
        print("tag:" + str(tagb))
        
        #check hit or miss
        flag = True
        count = 0
        linenum = 0 #hit line num
        val = 0 #number valid bits
        linenum2 = -1 #invalid/empty line number
        for x in self.storage[setb]:
            #line already in cache (write hit)
            if x.valid == 1 and tagb == x.tag:
                flag = True
                linenum = count
                break
            #line not found after looping through (write miss)
            else:
                flag = False
            
            #check if there is a missing line in cache
            if x.valid == 1:
                val += 1
            #get missing line number
            elif linenum2 == -1:
                linenum2 = count
            count += 1
        
        if flag == True:
            print("write_hit:yes")
            self.numHits += 1
            evict, dirty, address = self.write_hit(setb, tagb, blockb, data, linenum, add)
            
        else:
            print("write_hit:no")
            self.numMiss += 1
            evict, dirty = self.write_miss(setb, tagb, blockb, data, val, linenum2, add)
            
        print("eviction_line:" + str(evict))
        print("ram_address:" + str(address))
        print("data:" + self.convHex(data))
        print("dirty_bit:" + str(dirty))
    
    def write_hit(self, setb, tagb, blockb, inp, linenum, add):
        dirt = 0
        address = -1
        #write through policy
        if(self.hit == 1):
            line = self.storage[setb][linenum]
            line.uses += 1
            line.data[blockb] = inp
            
            self.mem[add] = inp
            address = add 

        #write back policy
        else:
            line = set.set(self.B)
            line = self.storage[setb][linenum]
            line.uses += 1
            line.data[blockb] = inp
            line.dirty = 1
            dirt = 1
        dataval = inp
        return  -1, dirt, address

    def write_miss(self, setb, tagb, blockb, data, val, linenum, add):
        evict = 0
        dirty = 0
        #evict invalid empty line first
        if val != self.E:
            evict = linenum
            self.write_dirty(self.storage[setb][evict], evict)
            dirty = self.write_allocate(setb, tagb, blockb, evict, add, data)
        else:
            #random replacement
            if self.rep == 1:
                evict = random.randint(0, self.E -1)
                self.write_dirty(self.storage[setb][evict], evict)
                dirty = self.write_allocate(setb, tagb, blockb, evict, add, data)

            #Least recently used
            else:
                least = self.storage[setb][0]
                count = 0
                for lines in self.storage[setb]:
                    if lines.uses < least.uses:
                        least = lines 
                        evict = count
                    count += 1
                self.write_dirty(self.storage[setb][evict], evict)
                dirty = self.write_allocate(setb, tagb, blockb, evict, add, data)
        return evict, dirty[1]
        
    #helper function writes data into cache
    def write_allocate(self, setb, tagb, blockb, linenum, add, data):
        dirty = 0
        #write allocate
        if self.miss == 1:
            
            # calc ram mem location
            tagbin = bin(tagb)[2:]
            setbin = bin(setb)[2:]
            total = (tagbin + setbin).ljust(self.membit, '0')
            tag = int(total, 2)
            count = 0
            block = []
            for val in self.mem[tag:tag + self.B]:
                block.append(val)
            
            #subtract uses from all lines
            for old in self.storage[setb]:
                old.uses -= 1

            #line to be put into cache set
            line = set.set(self.B)
            line.valid = 1
            line.tag = tagb
            line.uses = 1
            line.setBlock(block)
            self.storage[setb][linenum] = line 
            
            dirty = self.write_hit(setb, tagb, blockb, data, linenum, add)
            
        #no write allocate
        else:
            self.mem[add] = data
        return dirty

    #splits cache address into tag, set, and block offset
    def splitAddress(self, address):
        bits = []
        tBit = self.tagbit
        sBit = self.setbit
        bBit = self.blockbit
        tag = address[0 : tBit]
        Set = address[tBit : tBit+sBit]
        block = address[tBit+sBit : len(address)]
        bits.append(int(tag,2))
        bits.append(int(Set,2))
        bits.append(int(block,2))
        return bits

    # cache-dump - dumps data from cache storage into cache.txt
    def cDump(self):
        with open("cache.txt", 'w') as dump:
            for i, sets in enumerate(self.storage):
                for y, data in enumerate(sets):
                    line = data.getData()
                    dump.write(line)
    
    # cache-flush - clears the cache
    def flush(self):
        for i, sets in enumerate(self.storage):
            for y, data in enumerate(sets):
                # check for dirty bits
                if(data.dirty == 1 and data.valid == 1):
                    self.write_dirty(data, i)
                
                #clear cache line
                line = set.set(self.B)
                self.storage[i][y] = line
        print("cache-cleared")

    # replace ram with cache value if dirty and valid 
    # data is set line, i is the set number
    def write_dirty(self, data, i):
        if(data.dirty == 1 and data.valid == 1):
            # calc ram mem location
            tagb = bin(data.tag)[2:]
            setb = bin(i)[2:]
            total = (tagb + setb).ljust(self.membit, '0')
            add = int(total, 2)
            
            #loop through ram and replace block
            for num, val in enumerate(self.mem[add:add + self.B]):
                self.mem[add+num] = data.data[num]
        return

    # cache-view - displays data in cache and cache configuration
    def cView(self):
        #string concatenation for configuration
        size = "cache_size:" + str(self.size)
        block = "data_block_size:" + str(self.B)
        assoc = "associativity:" + str(self.E)
        if(self.rep == 1):
            repPol = "random_replacement"
        else:
            repPol = "least_recently_used"
        
        if(self.hit == 1):
            hitPol = "write_through"
        else:
            hitPol = "write_back"

        if(self.miss == 1):
            missPol = "write_allocate"
        else:
            missPol = "no_write_allocate"
        repl = "replacement_policy:" + repPol
        hitl = "write_hit_policy:" + hitPol
        missl = "write_miss_policy:" + missPol
        prinHits = "num_of_cache_hits:" + str(self.numHits)
        prinMiss = "num_of_cache_misses:" + str(self.numMiss)

        print(size)
        print(block)
        print(assoc)
        print(repl)
        print(hitl)
        print(missl)
        print(prinHits)
        print(prinMiss)

        #prints cache contents and identifying bits
        print("cache_content:")
        for sets in self.storage:
            for line in sets:
                line.printLine()

    def convHex(self, num):
        return "0x" + num
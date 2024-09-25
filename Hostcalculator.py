#!/usr/bin/python3

"""
A simple host calculator for lazy network people. with no imports/dependency required.

Usage:

import Hostcalculator

object_name = Hostcalculator.hosts()#to run hosts table from __init__
"""


class hosts:
    #ALDEERAN PLANET 
    def cidr_to_fullmask(self, cidr):

        #"{:032d}".format(int("1"*cidr))[::-1]
        pass
        #returns a 2D array [hosts [whole subnet]]
        return self.subnets[int(cidr)]

    def calculate_nflb(self, ip, cidr):
        self.ip = str(ip)
        self.cidr = int(cidr)
        pass


    def __init__(self, verbose=False):

        self.subnets = {} #will get populated once imported. (init)
        self.verbose = verbose
        #'{:032d}'.format(int("1"*cidr))[::-1]
        #[subnet[i:i+8] for i in range(0, len(subnet), 8)]

        for i in range(32):
            #no dependency quick and dirty way to convert a cidr to 
            #a subnet mask
            long_subnet =  "{:032d}".format( int("1"* (i+1) ) )[::-1]
            long_subnet =   [long_subnet[i:i+8] for i in range(0, len(long_subnet), 8)] 
            long_subnet = [int(("0b" +octet), 2) for octet in long_subnet]
            
            self.subnets.update({32-i : [2**i, long_subnet]})

        if self.verbose== True: 
            for keys, value in self.subnets.items():
                print(keys, "=>", value)
                pass

    

        #print(self.subnets)



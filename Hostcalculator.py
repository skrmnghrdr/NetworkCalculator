#!/usr/bin/python3

"""
A simple host calculator for lazy network people. with no imports/dependency required.

Usage:

import Hostcalculator

object_name = Hostcalculator.hosts()#to run hosts table from __init__
"""


class hosts:

    def cidr_to_fullmask(self, cidr):

        #returns a 2D array [hosts [whole subnet]]
        return self.subnets[int(cidr)]

    def calculate_nflb(self, ip, cidr):
        self.ip = str(ip)
        self.cidr = int(cidr)

        self.last_assignable = ""
        self.first_assignable = ""
        self.networkaddr = ""
        self.broadcast = ""
        #use and method to get the network
        """
        logic plan
        put long subnets in binary
        1111 1111.1111 1111.1111 1111.0000 0000
        NETWORK AND BROADCAST
        work with the most significant bit turned on; on that octet
        increment by that octet.

        TODO: Fix the long subnet,
        also fix the hosts to correspond with the cidr, somehow off by 1
        """
        


    def __init__(self, verbose=True):

        self.subnets = {} #will get populated once imported. (init)
        self.verbose = verbose

        for i in range(32, 0, -1):
            #no dependency quick and dirty way to convert a cidr to 
            #a subnet mask


            long_subnet =  "{:031d}".format( int("1"* (i) ) )[::-1]
            #print all the bits and pad it with 0. [::-1] cause it pads it from the left
            long_subnet =   [long_subnet[i:i+8] for i in range(0, len(long_subnet), 8)]
            #get octet by 8 (see the 8 at the end of the range()) 
            pass
            long_subnet = [int(("0b" +octet), 2) for octet in long_subnet]
            #manually add 0b then convert to base10 
            


            self.subnets.update({33-i : [2**i, long_subnet]})
            pass
        if self.verbose== True: 
            for keys, value in self.subnets.items():
                print(keys, "=>", value)
                pass

    

        #print(self.subnets)



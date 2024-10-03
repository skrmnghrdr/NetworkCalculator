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
        
    def populate_subnet_table(self):

        self.subnets = {}
        for i in range(32, 0, -1):
            #no dependency quick and dirty way to convert a cidr to 
            #a subnet mask

            long_subnet =  "{:032d}".format( int("1"*(i) ) )[::-1]
            #print all the bits and pad it with 0. [::-1] cause it pads it from the left
            long_subnet =   [long_subnet[i:i+8] for i in range(0, len(long_subnet), 8)]
            #get octet by 8 (see the 8 at the end of the range()) 
            long_subnet = [int(("0b" +octet), 2) for octet in long_subnet]
            #manually add 0b then convert to base10 

            projected_hosts = 2**((i-32)*-1)
            self.subnets.update({i : [projected_hosts, long_subnet]})
        if self.verbose== True: 
            for keys, value in self.subnets.items():
                print(keys, "=>", value)
                

        self.subnets.update({0 : [2**32, "0.0.0.0"]})


    def __init__(self, verbose=True):
        self.verbose = verbose
        self.populate_subnet_table()
        pass
        #print(self.subnets)



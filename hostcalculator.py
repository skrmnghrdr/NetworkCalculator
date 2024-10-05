#!/usr/bin/python3

"""
A simple host calculator for lazy network people. with no imports/dependency required.

functions return as dicts which are API friendly

Usage:

import Hostcalculator

object_name = Hostcalculator.hosts()
"""


class hosts:

    def cidr_to_fullmask(self, cidr):

        #returns a 2D array [hosts [whole subnet]]
        fullmask_and_hosts = self.subnets[int(cidr)]
        long_subnet_string = ".".join([str(x) for x in fullmask_and_hosts[1]])

        if self.verbose == True:
            print("CIDR: {0} Available hosts: {1}, Long Subnet: {2}".format(
                str(cidr), 
                str(fullmask_and_hosts[0]),
                long_subnet_string
                ))
            
        return fullmask_and_hosts


    def calculate_nflb(self, ip, subnet):
        """
        Accepts both cidr and long subnet as a string
        """

        if type(subnet) == int:
            #from subnet dictionary, get cidr and long subnet
            subnet = self.subnets[subnet][1]

        #TODO
        #start to get the network IP first:
        #bin(255) and 0b11111100 
        #0b11111100 and 0b11111100 #both work
        
        self.last_assignable = ""
        self.first_assignable = ""
        self.networkaddr = ""
        self.broadcast = ""        
        
        
        
        self.ip = str(ip)
        self.cidr = int(cidr)

        #use and method to get the network
        """
        logic plan
        put long subnets in binary
        1111 1111.1111 1111.1111 1111.0000 0000
        NETWORK AND BROADCAST
        work with the most significant bit turned on; on that octet
        increment by that octet.

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

        self.subnets.update({0 : [2**32,[0,0,0,0] ]})

        if self.verbose== True: 
            for keys, value in self.subnets.items():
                print(keys, "=>", value)
 

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.populate_subnet_table()
        print('Object created')

        pass


if __name__ == "__main__":
    pass
    #test environment
    #hosts(verbose=True).cidr_to_fullmask(24)
    hosts(verbose=True).calculate_nflb("192.168.1.0", 32)
    pass
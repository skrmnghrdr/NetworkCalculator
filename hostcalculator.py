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
        Accepts both (int)cidr and (string)long subnet
        """
        #"{:(direction of fill, < or >)(fill)(len)}".format("appears on the colon")
        #"{:>019}".format("22aaaaaaaaa")
        self.NFLB = {}
        if type(subnet) == int:
            self.NFLB.update({
                "CIDR" : str(subnet),
                "subnet" : self.subnets[subnet][1] #PLEASE CONVERT TO STRING LATER
            })
            #from subnet dictionary, get cidr and long subnet         
            self.subnet =  ["{:<08}".format(bin(int(x))[2:]) for x in self.subnets[subnet][1]]
            pass
        else:
            self.NFLB.update({
                "subnet" : subnet,
            })
            #just convert the dec to bin
            self.subnet =  ["{:<08}".format(bin(int(x))[2:]) for x in subnet.split('.')]
            
        self.ip = ["{:>08}".format(bin(int(x))[2:]) for x in ip.split('.')]
        self.networkaddress = ''.join( [bin(int(x,2) & int(y,2))[2:].zfill(8) for x, y in zip(self.ip, self.subnet)] )

        self.host_bits = []
        #determine the NEXT network address
        for octet in self.subnet:
            if octet == "11111111":
                #if 255, then just append the 0
                self.host_bits.append("00000000")
            else:

                current_octet_host = ""
                for bit in octet:
                    #we inverse it manually because ~ operator
                    #does not work for python3 uses signed ints
                    if int(bit) == 1:
                        current_octet_host += "0"
                    if int(bit) == 0:
                        current_octet_host += "1"
                self.host_bits.append(current_octet_host)

        #Will need to find a way to +1 on the network and -1 on the broadcast to get
        #the two remaining things

        self.broadcast = "".join('1' if ''.join(self.ip)[i] == '1' or ''.join(self.host_bits)[i] == '1' else '0' for i in range(32))      
        


        carry = 1 #initial 1 cause we need to add 1
        projected_first_assignable = ""
        current_bit_position = 0

        #might use enumerate, save the indexes, for subtracting
        for i in range(len(self.networkaddress)): 
            #could use a bitwise addititon but we'll do it manually anyways
          
            if int(self.networkaddress[::-1][i]) == 1 and carry == 1:
                print(int(self.networkaddress[::-1][i]))
                #we add them both
                projected_first_assignable += "0"
                continue
            elif int(self.networkaddress[::-1][i]) == 0 and carry == 1:
                print(int(self.networkaddress[::-1][i]))
                projected_first_assignable += "1"
                carry = 0
            elif int(self.networkaddress[::-1][i]) == 1 and carry == 0:
                projected_first_assignable += "1"
            elif int(self.networkaddress[::-1][i]) == 0 and carry == 0:
                projected_first_assignable += "0"
        pass 
        self.first_assignable = projected_first_assignable[::-1]

        #messy, but converts long 32bit to 4 octet then put as decimal
        #self.first_assignable = [int(("0b"+octet), 2) for octet in [self.first_assignable[i:i+8] for i in range(0, len(self.first_assignable), 8)]]
        
        #calculate the last assignable
        borrowed_bit_index = 0
        projected_last_assignable = ""

        #find the first significant bit
        for index, bit in enumerate(self.broadcast[::-1]):
            if int(bit): #if 1
                print('1 true ran')
                borrowed_bit_index = index
                projected_last_assignable = "0"
                pass
                projected_last_assignable += (("1" * borrowed_bit_index) )
                break
            elif not int(bit): #0
                print('NOT RAN')
                current_index = index


        projected_last_assignable = "{1}{0}".format(self.broadcast[::-1][(borrowed_bit_index+1):],projected_last_assignable)
        projected_last_assignable = [int(("0b"+octet), 2) for octet in [projected_last_assignable[::-1][i:i+8] for i in range(0, len(projected_last_assignable), 8)]]

        #uncomment this for DDN broadcast.
        #pretty dirty and unarranged. :(
        print('debug')

        self.last_assignable = ".".join(str(x) for x in projected_last_assignable)
        self.first_assignable = [int(("0b"+octet), 2) for octet in [self.first_assignable[i:i+8] for i in range(0, len(self.first_assignable), 8)]]
        self.broadcast = ".".join(str(int(self.broadcast[i:i+8], 2)) for i in range(0, 32, 8))
        self.networkaddress = ".".join(str(x) for x in [int(("0b"+octet), 2) for octet in [self.networkaddress[i:i+8] for i in range(0, 32, 8) ]])

        self.NFLB.update({
            "ip" : ip,
            "network" : self.networkaddress,
            "first" : self.first_assignable,
            "last" : self.last_assignable,
            "broadcast" : self.broadcast,
        })

        return self.NFLB
        pass

    def populate_subnet_table(self):

        self.subnets = {}
        for i in range(32, 0, -1):
            #no dependency quick and dirty way to convert a cidr to 
            #a subnet mask

            long_subnet =  "{:032d}".format( int("1"*(i) ) )[::-1]
            on_bits = long_subnet
            #print all the bits and pad it with 0. [::-1] cause it pads it from the left
            long_subnet =   [long_subnet[i:i+8] for i in range(0, len(long_subnet), 8)]
            #get octet by 8 (see the 8 at the end of the range()) 
            long_subnet = [int(("0b" +octet), 2) for octet in long_subnet]
            #manually add 0b then convert to base10 

            projected_hosts = 2**((i-32)*-1)
            self.subnets.update({i : [projected_hosts, long_subnet, on_bits]})

        self.subnets.update({0 : [2**32,[0,0,0,0], ("0"*32) ]})

        if self.verbose== True: 
            for keys, value in self.subnets.items():
                print(keys, "=>", value)
 

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.populate_subnet_table()
        print('Object created')

if __name__ == "__main__":
    #test environment
    #hosts(verbose=True).cidr_to_fullmask(24)
    hosts(verbose=False).calculate_nflb("192.168.0.0", 18)
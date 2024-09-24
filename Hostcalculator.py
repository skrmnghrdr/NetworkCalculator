#!/usr/bin/python3

"""
A simple host calculator for lazy network people.
"""


class hosts:

    def cidr_to_fullmask(cidr):
        pass
        

    def __init__(self):

        self.subnets = {} #will get populated once imported. (init)
        
        for i in range(32):
            self.subnets.update({32-i : 2**i})
            
        for keys, value in self.subnets.items():
            print(keys, "=>", value)


        #print(self.subnets)



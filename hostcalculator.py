#!/usr/bin/python3

class hosts:
    """
        A simple host calculator for network people. 100% python3 with no imports/dependency required.
        Usage:
        import Hostcalculator

        object_name = Hostcalculator.hosts(verbose=False)
        object_name.calculate_nflb(str:ip, str:subnet OR int:cidr)

    """
    def cidr_to_fullmask(self, cidr):
        """returns a 2D array [hosts [whole subnet]]"""
        fullmask_and_hosts = self.subnets[int(cidr)]
        long_subnet_string = ".".join([str(x) for x in fullmask_and_hosts[1]])

        if self.verbose == True:
            print("CIDR: {0} Available hosts: {1}, Long Subnet: {2}".format(
                str(cidr), 
                str(fullmask_and_hosts[0]),
                long_subnet_string
                ))
            
        return fullmask_and_hosts

    def fullmask_to_cidr(self, fullmask):
        """returns a string form of CIDR"""
        fullmask = [int(x) for x in fullmask.split('.')]
        for index, (key, value) in enumerate(self.subnets.items()):
            if fullmask == value[1]:
                return str(key)
            
        return {"error": {"message" : "Invalid subnet mask"}}

    def calculate_nflb(self, ip, subnet):
        """
        Accepts both (int)cidr and (string)long subnet:
        returns a DICT{
            "ip" : str,
            "CIDR" : str,
            "subnet" : str,
            "network" : str,
            "hosts" : str,
            "first" : str,
            "last" : str,
            "broadcast" : str,
        }
        """
    
        #"{:(direction of fill, < or >)(fill)(len)}".format("appears on the colon")
        #"{:>019}".format("22aaaaaaaaa")
        self.NFLB = {}
        if type(subnet) == int:
            self.NFLB.update({
                "CIDR" : str(subnet),
                #HERE DEBUG
                "subnet" : '.'.join(map(str, self.cidr_to_fullmask(subnet)[1]))
            })
            #from subnet dictionary, get cidr and long subnet         
            self.subnet =  ["{:<08}".format(bin(int(x))[2:]) for x in self.subnets[subnet][1]]
            pass
        else:
            self.NFLB.update({
                "CIDR" : self.fullmask_to_cidr(subnet),
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

        self.broadcast = "".join('1' if ''.join(self.ip)[i] == '1' or ''.join(self.host_bits)[i] == '1' else '0' for i in range(32))      
        
        carry = 1 #initial 1 cause we need to add 1
        projected_first_assignable = ""
        current_bit_position = 0

        for i in range(len(self.networkaddress)): 
            #could use a bitwise addititon but we'll do it manually anyways
            if int(self.networkaddress[::-1][i]) == 1 and carry == 1:
                if self.verbose == True:
                    print(int(self.networkaddress[::-1][i]))
                #we add them both
                projected_first_assignable += "0"
                continue
            elif int(self.networkaddress[::-1][i]) == 0 and carry == 1:
                if self.verbose == True:
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

        #calculate the last assignable
        borrowed_bit_index = 0
        projected_last_assignable = ""

        #find the first significant bit
        for index, bit in enumerate(self.broadcast[::-1]):
            if int(bit): #if 1
                borrowed_bit_index = index
                projected_last_assignable = "0"
                pass
                projected_last_assignable += (("1" * borrowed_bit_index) )
                break
            elif not int(bit): #0
                current_index = index

        #finalize the output (i'm sorry)
        projected_last_assignable = "{1}{0}".format(self.broadcast[::-1][(borrowed_bit_index+1):],projected_last_assignable)
        projected_last_assignable = [int(("0b"+octet), 2) for octet in [projected_last_assignable[::-1][i:i+8] for i in range(0, len(projected_last_assignable), 8)]]
        self.last_assignable = ".".join(str(x) for x in projected_last_assignable)
        self.first_assignable = [int(("0b"+octet), 2) for octet in [self.first_assignable[i:i+8] for i in range(0, len(self.first_assignable), 8)]]
        self.first_assignable = '.'.join(map(str, self.first_assignable))
        self.broadcast = ".".join(str(int(self.broadcast[i:i+8], 2)) for i in range(0, 32, 8))
        self.networkaddress = ".".join(str(x) for x in [int(("0b"+octet), 2) for octet in [self.networkaddress[i:i+8] for i in range(0, 32, 8) ]])

        self.NFLB.update({
            "ip" : ip,
            #updated above
            #"CIDR" : "cidr",
            #"subnet" : "subnet",
            "network" : self.networkaddress,
            "hosts" : str(self.subnets[int(self.NFLB["CIDR"])][0]),
            "first" : self.first_assignable,
            "last" : self.last_assignable,
            "broadcast" : self.broadcast,
        })

        return self.NFLB

    def populate_subnet_table(self):
        """This method runs after creating an instance.
        It is used to populate the whole hosts table from /32 to /0
        DICT FORMAT:
        {
        int(CIDR) :[int(hosts) [long_subnet],
        str(subnetbits)]
        }
        """
        self.subnets = {}
        for i in range(32, 0, -1):

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
    #pass
    print('Please see documentation for usage')
    #hosts(verbose=False).calculate_nflb("192.168.0.0", "255.255.255.0")

def main(): 
    global add_ava
    start = []
    host_nums = []
    add_ava = valid_ip() #Gets a valid IP Address and Prefix
    while host_nums == []: #Loops until valid host requirements are given
        host_nums = hosts_req()
    for i in range (len(add_ava)): #Creates a new list with the data from add_ava
        start.append(int(add_ava[i])) 
    for i in range(len(host_nums)): #Loops until all subnets are made
        network_address = list_to_address(start) #records the network address
        first_address = next_network_address(start) #Gets the first address
        first_address = list_to_address(first_address) #records the first address
        start = prev_network_address(start)
        needed_num = 2
        host_bits = 1
        seg_num = 3
        while  host_nums[i] > needed_num - 2: #Loops until a power of 2 is found which is
            host_bits += 1                    #greater than the host requirement
            needed_num = 2**host_bits
        subnet_mask = find_mask(host_bits) #Finds the subnet mask
        prefix = "/"+str(32-host_bits) #Finds new prefix
        num_of_use = needed_num - 2
        while host_bits > 8: #Finds out how much to add for each segment
            if host_bits > 8:
                host_bits -= 8
                start[seg_num]+= 2**(8)-1
            seg_num -= 1
        start[seg_num] += 2**(host_bits)-1  
        broadcast_address = list_to_address(start) #records broadcast address
        last_address = prev_network_address(start) #finds last address
        last_address = list_to_address(last_address) #records last address
        subnet_mask = list_to_address(subnet_mask) #records subnetmask
        for x in range(2):
            start = next_network_address(start) #finds next network address
        #Prints Data
        print ("Subnet "+str(i+1)+" ("+str(host_nums[i])+" Hosts Wanted)")
        print ("Network Address: "+str(network_address)+prefix)
        print ("First Usable Address: "+str(first_address)+prefix)
        print ("Last Usable Address: "+str(last_address)+prefix)
        print ("Broadcast Address: "+str(broadcast_address)+prefix)
        print ("Subnet Mask: "+str(subnet_mask))
        print ("Number of Addresses: "+str(needed_num))
        print ("Number of Usable Addresses: "+str(num_of_use))
        print ("\n")
    
def valid_ip():
    address = ""
    while address == "": 
        address = input("Please input the IP Address: ")
        print ("")
        i = 0
        if (address.count(".")!= 3 or len(address)<9 or address[0] == "."
            or address.count("/")!= 1 or address[0] == "/"):
            address = ""
        
        while i < len(address) and address != "":
            if not(address[i].isdigit() or address[i] == "." or  address[i] == "/"):
                address = ""
            if (address[i:i+2] == ".." or address[i:i+2] == "//" or
                address[i:i+2] == "/." or address[i:i+2] == "./"):
                address = ""
            if address[i:i+4].isdigit() and not (i>len(address)-4):
                address = ""
            if address[i:i+3].isdigit():
                num = int(address[i:i+3])
                if not(-1<num<256):
                    address = ""

            i += 1
        prefix = address[-2:]
        address = address[:-3]
        address = address.split(".")
        address.append(prefix)
        for i in range (len(address)):
            if address[i].isdigit():
                address[i] = int(address[i])   
        try:
            if 24<=address[4]<=31:
                check = 3
            elif 16<=address[4]<=23:
                check = 2
            elif 8<=address[4]<=15:
                check = 1
            else:
                check = 0
        except:
            address = ""
            check = 0
        try:
            net_check = 2**((32 - address[4])%8)
            if net_check == 1:
                net_check = 256
            if not(address[check]%net_check == 0):
                address = ""
            if address != "":
                for i in range(3-check):
                    if address[3-i] != 0:
                        address = ""
                        i = 3
        except:
            address = ""
        if address == "":
            print("Invalid Address\n")
    
    return address

def hosts_req():
    num_of_hosts = 1
    host_num_list = []
    while num_of_hosts != 0:
        num_of_hosts = input("Enter the Number of Hosts per Subnet [Print 0 to Stop Entering Host Numbers]: ")
        if num_of_hosts.isdigit():
            num_of_hosts = int(num_of_hosts)
            if num_of_hosts != 0:
                host_num_list.append(num_of_hosts)
        elif num_of_hosts == "b":
            print()
            main()
        else:
            print("Invalid Host Entered")
    total = 0
    for i in range(len(host_num_list)):
        needed = 1
        while host_num_list[i] + 2 >= needed:
            needed *= 2
        total += needed
    if total >  2**(32-add_ava[4]):
        print("\nToo Many Hosts")
        host_num_list = []
    else:
        host_num_list.sort(reverse = True)
    print("\n")
    return host_num_list
        
def list_to_address(list_address):
    str_address = ""
    for i in range(4):
        str_address += str(list_address[i])
        if i != 3:
            str_address += "."
    return str_address

def next_network_address(address):
    address[3] += 1
    remainder = True
    i = 3
    while remainder:
        remainder = False
        if address[i] == 256:
            remainder = True
            address[i] = 0
            address[i-1] += 1
            i -= 1
    return address

def prev_network_address(address):
    address[3] -= 1
    remainder = True
    i = 3
    while remainder:
        remainder = False
        if address[i] == -1:
            remainder = True
            address[i] = 255
            address[i-1] -= 1
            i -= 1
    return address

def find_mask(host_bits):
    subnet_mask_list = []
    segment_num = 255
    network_bits = 32 - host_bits
    while network_bits>8: #For every 8 bits record 255 for each subnet segment
        subnet_mask_list.append(segment_num)
        network_bits -= 8
    for i in range(network_bits): #Finds out the segment which isn't 255 or 0
        segment_num += 2**(7-i)
    segment_num -= 255
    subnet_mask_list.append(segment_num) #Adds segments which is supposed to be 0
    for i in range (4 -len(subnet_mask_list)):
        subnet_mask_list.append(0)
    return subnet_mask_list

if __name__ == "__main__":
    main()
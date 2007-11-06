#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

from os import popen

def get_local_ipv4_addresses():
    iplist = []

    iphandle = popen("ip addr show scope global")
    while 1:
        line = iphandle.readline()
        if not line:
            break

        tag = "inet "
        tagstart = line.find(tag)
        if tagstart == -1:
            continue

        slash = line.find("/")

        ip = line[tagstart + len(tag):slash]
        iplist.append(ip)
    iphandle.close()

    return iplist

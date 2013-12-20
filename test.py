#!/usr/bin/env python

import glusterwrap as gw
import json
import datetime 

def print_list(objList):
    jsonDumpsIndentStr = json.dumps(objList, indent=1)
    print jsonDumpsIndentStr

if __name__ == "__main__":
#    peer_status = gw.peer.status(remotehost=gw.util.get_ip())
#    print_list(peer_status)
#    print '-------------'
#    volume_status = gw.volume.info(remotehost=gw.util.get_ip())
#    print 'volume status:'
#    print_list(volume_status)

     [flag, msg] = gw.peer.detach(hostname="localhost", targetname="10.0.0.240")
     print flag
     print msg
    

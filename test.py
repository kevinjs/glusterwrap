#!/usr/bin/env python

import glusterwrap as gw
import json
import datetime 

def print_list(objList):
    jsonDumpsIndentStr = json.dumps(objList, indent=1)
    print jsonDumpsIndentStr

if __name__ == "__main__":
#    t1 = datetime.datetime.now()
#    peer_status_v2 = gluster.peer.status_v2(remotehost='10.0.0.54')
#    t2 = datetime.datetime.now()
    peer_status = gw.peer.status(remotehost='10.0.0.54')
#    t3 = datetime.datetime.now()
#    print 'peer status_v2:'
#    print_list(peer_status_v2)
    print 'peer status:'
    print_list(peer_status)
#    print 'status_v2 cost: ' + str((t2 - t1).microseconds)
#    print 'status: ' + str((t3 - t2).microseconds)

    print '-------------'
    volume_status = gw.volume.info()
    print 'volume status:'
    print_list(volume_status)
    

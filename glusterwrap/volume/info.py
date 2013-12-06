# -*- encoding: utf-8 -*
# Copyright © 2013 Computer Network Information Center, Chinese Academy of Sciences
#
# Author: Jing Shao <jingshao@cnic.cn>

import re
import glusterwrap as gw

def info(volname="all",remotehost="localhost"):
    """
    Retrieve the volume information
    Returns a dict in the form of:
    {
     "timestamp": "2013-12-06 08:46:45", 
     "state": "NORMAL", 
     "volinfo": {
      "data_backup": {
       "status": "Started", 
       "bricks": [
        "10.0.0.54:/data/back", 
        "10.0.0.48:/data/back", 
        "10.0.0.60:/data/back"
       ], 
       "timestamp": "2013-12-06 08:46:45", 
       "volname": "data_backup", 
       "type": "Replicate", 
       "options": {}, 
       "transport": [
        "tcp"
       ]
      }, 
      "data_volume": {
       "status": "Started", 
       "bricks": [
        "10.0.0.48:/data/gluster", 
        "10.0.0.60:/data/gluster"
       ], 
       "timestamp": "2013-12-06 08:46:45", 
       "volname": "data_volume", 
       "type": "Replicate", 
       "options": {}, 
       "transport": [
        "tcp"
       ]
      }
     }, 
     "reportor": "192.168.75.64", 
     "volumes": 2
    }
    If ``remotehost`` is set, volume info will be retrieved from the remote host.
    """
    return _info(volname, remotehost)

def _info(volname="all",remotehost="localhost"):
    # Initialize
    volumes = {"volumes":0, 
               "reportor":remotehost, 
               "timestamp":gw.util.get_now(),
               "state":"NORMAL",
               "volinfo":{}}

    # Prepare process cmd
    gluster_path = None
    tmp_list = gw.util.which('gluster')
    if tmp_list != [] and tmp_list != None:
        gluster_path = tmp_list[0]
    else:
        return {}

    program = [gluster_path,
            "--remote-host=%s" % remotehost, 
            "volume", 
            "info",
            volname]

    response = gw.util.do_process(program)    

    if response != None:
        for line in response:
            m = re.match("Volume Name: (.+)",line)
            if m:
                volname = m.group(1)
                volumes['volumes'] = volumes['volumes'] + 1
                volumes["volinfo"][volname] = {"bricks": [], "options": {}}
                volumes["volinfo"][volname]["timestamp"] = gw.util.get_now()
                volumes["volinfo"][volname]["volname"] = volname
            m = re.match("Type: (.+)",line)
            if m:
                volumes["volinfo"][volname]["type"] = m.group(1)
            m = re.match("Status: (.+)",line)
            if m:
                volumes["volinfo"][volname]["status"] = m.group(1)
            m = re.match("Transport-type: (.+)",line)
            if m:
                volumes["volinfo"][volname]["transport"] = [x.strip() for x in m.group(1).split(",")]
            m = re.match("Brick[1-9][0-9]*: (.+)",line)
            if m:
                volumes["volinfo"][volname]["bricks"].append(m.group(1))
            m = re.match("^([-.a-z]+: .+)$",line)
            if m:
                opt,value = [x.strip() for x in m.group(1).split(":")]
                volumes["volinfo"][volname]["options"][opt] = value
    else:
        volumes['state'] = "LOCAL_GLUSTER_STOP"
    return volumes

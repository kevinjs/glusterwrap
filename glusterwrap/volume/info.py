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
    If ``remotehost`` is set, volume info will be retrieved from the remote host.
    """
    return _info(volname, remotehost)

def _info(volname="all",remotehost="localhost"):
    # Initialize
    volumes = {"volumes":0, 
               "reportor":remotehost, 
               "timestamp":gw.util.get_now(),
               "state":"NORMAL"}

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
                volumes[volname] = {"bricks": [], "options": {}}
                volumes[volname]["timestamp"] = gw.util.get_now()
            m = re.match("Type: (.+)",line)
            if m:
                volumes[volname]["type"] = m.group(1)
            m = re.match("Status: (.+)",line)
            if m:
                volumes[volname]["status"] = m.group(1)
            m = re.match("Transport-type: (.+)",line)
            if m:
                volumes[volname]["transport"] = [x.strip() for x in m.group(1).split(",")]
            m = re.match("Brick[1-9][0-9]*: (.+)",line)
            if m:
                volumes[volname]["bricks"].append(m.group(1))
            m = re.match("^([-.a-z]+: .+)$",line)
            if m:
                opt,value = [x.strip() for x in m.group(1).split(":")]
                volumes[volname]["options"][opt] = value
    else:
        volumes['state'] = "LOCAL_GLUSTER_STOP"
    return volumes

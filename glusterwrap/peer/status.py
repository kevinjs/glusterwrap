# -*- encoding: utf-8 -*
# Copyright © 2013 Computer Network Information Center, Chinese Academy of Sciences
#
# Author: Jing Shao <jingshao@cnic.cn>

import re
import glusterwrap as gw

def status(remotehost="localhost"):
    """
    Retrieve the status of the peer group.

    Returns a dict in the form of:
    {
     "peerstatus": {
      "10.0.0.60": {
       "timestamp": "2013-12-04 16:49:26", 
       "host": "10.0.0.60", 
       "uuid": "3e9ba3a8-32ba-48db-8a01-95c563a1d476", 
       "state": "Peer in Cluster (Connected)"
      }, 
      "10.0.0.48": {
       "timestamp": "2013-12-04 16:49:26", 
       "host": "10.0.0.48", 
       "uuid": "08845703-39c2-466b-9fe5-24ae42969dd0", 
       "state": "Peer in Cluster (Connected)"
      }, 
      "10.0.0.54": {
       "timestamp": "2013-12-04 16:49:26", 
       "host": "10.0.0.54", 
       "uuid": "82f40521-297b-4605-ae57-2c54ca9cdae0", 
       "state": "Peer in Cluster (Connected)"
      }
     }, 
     "peers": 3
    }
    """
    return _status(remotehost)

def _status(remotehost="localhost", recursion=False):
    peerstatus = {"peerstatus": {}, "peers":0}

    # Get gluster cmd path
    gluster_path = None
    tmp_list = gw.util.which('gluster')
    if tmp_list != [] and tmp_list != None:
        gluster_path = tmp_list[0]
    else:
        # There is no gluster on this server
        return None
    
    program = [gluster_path,
            "--remote-host=%s" % remotehost,
            "peer",
            "status"]

    init_status = gw.util.do_process(program)

    #import pdb;pdb.set_trace()

    if init_status != None:
        # Initialize 1st node
        tmp_self = {}
        tmp_self["host"] = remotehost
        tmp_self["timestamp"] = gw.util.get_now()
        tmp_self["uuid"] = ""
        tmp_self["local"] = True
        tmp_self["state"] = "Peer in Cluster (Connected)"

        hostlist = []
        # step through the output and build the dict
        for line in init_status:
            if line.count("No peers present") != 0:
                peerstatus["peers"] = 0
                peerstatus["state"] = "NO_PEERS_PRESENT"
                return peerstatus
            m = re.match("^Number of Peers: (\d+)$", line)
            if m:
                peerstatus["peers"] = int(m.group(1)) + 1
            m = re.match("^Hostname: (.+)$", line)
            if m:
                hostname = m.group(1)
                hostlist.append(hostname)
                peerstatus["peerstatus"][hostname] = {}
                peerstatus["peerstatus"][hostname]["host"] = hostname
                peerstatus["peerstatus"][hostname]["local"] = False
                peerstatus["peerstatus"][hostname]["timestamp"] = gw.util.get_now()
            m = re.match("Uuid: ([-0-9a-f]+)", line)
            if m:
                peerstatus["peerstatus"][hostname]["uuid"] = m.group(1)
            m = re.match("State: (.+)", line)
            if m:
                peerstatus["peerstatus"][hostname]["state"] = m.group(1)

        # get local peer info from other live node
        has_self = False
        for host in hostlist:
            # skip disconnected node
            if peerstatus["peerstatus"][host]["state"] != "Peer in Cluster (Disconnected)":
                program = [gluster_path,
                "--remote-host=%s" % host,
                "peer",
                "status"]
                remote_status = gw.util.do_process(program)
                if remote_status != None:
                    for line in remote_status:
                        m = re.match("^Hostname: (.+)$", line)
                        if m:
                            hostname = m.group(1)
                        if hostname not in hostlist and \
                             not peerstatus["peerstatus"].has_key(hostname):
                            peerstatus["peerstatus"][hostname] = {}
                            peerstatus["peerstatus"][hostname]["host"] = hostname
                        m = re.match("Uuid: ([-0-9a-f]+)", line)
                        if m and \
                             hostname not in hostlist and \
                             not peerstatus["peerstatus"][hostname].has_key("timestamp"):
                            peerstatus["peerstatus"][hostname]["timestamp"] = gw.util.get_now()
                            peerstatus["peerstatus"][hostname]["uuid"] = m.group(1)
                        m = re.match("State: (.+)", line)
                        if m and \
                             hostname not in hostlist and \
                             not peerstatus["peerstatus"][hostname].has_key("state"):
                            peerstatus["peerstatus"][hostname]["state"] = m.group(1)
                            peerstatus["peerstatus"][hostname]["local"] = True
                            has_self = True
                            hostlist.append(hostname)
                            break;
            else:
                has_self = False
                continue
            if has_self:
                break

            # If other node are all disconnected
        peerstatus["state"] = "NORMAL"
        if not has_self:
            peerstatus["peerstatus"][remotehost] = tmp_self
            peerstatus["state"] = "ONLY_SELF"
        peerstatus["peers"] = len(peerstatus["peerstatus"])
    else:
        # service gluster on this server is shutdown.
        peerstatus['peerstatus'][remotehost] = {}
        peerstatus["peerstatus"][remotehost]["host"] = remotehost
        peerstatus["peerstatus"][remotehost]["state"] = "Local gluster stop"
        peerstatus["peerstatus"][remotehost]["local"] = True
        peerstatus["peerstatus"][remotehost]["uuid"] = ""
        peerstatus["peerstatus"][remotehost]["timestamp"] = gw.util.get_now()
        peerstatus["state"] = "LOCAL_GLUSTER_STOP"
    return peerstatus
       

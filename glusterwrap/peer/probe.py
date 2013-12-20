# -*- encoding: utf-8 -*
# Copyright © 2013 Computer Network Information Center, Chinese Academy of Sciences
#
# Author: Jing Shao <jingshao@cnic.cn>

import re
import glusterwrap as gw

def probe(hostname, targetname):
    return _probe(hostname=hostname, targetname=targetname)

def _probe(hostname, targetname):
    # Get gluster cmd path
    gluster_path = None
    tmp_list = gw.util.which('gluster')
    if tmp_list != [] and tmp_list != None:
        gluster_path = tmp_list[0]
    else:
        # There is no gluster on this server
        return None
    
    program = [gluster_path,
            "--remote-host=%s" % hostname,
            "peer",
            "probe",
            targetname]

    response = gw.util.do_process_resp(program)

    if response == None:
        return [False, "Run subprocess error."]
    else:
        if response[0].count('success') > 0:
            return [True, response]
        else:
            return [False, response]

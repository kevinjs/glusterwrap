# -*- encoding: utf-8 -*
# Copyright © 2013 Computer Network Information Center, Chinese Academy of Sciences
#
# Author: Jing Shao <jingshao@cnic.cn>

import os
import os.path
import datetime, time
import subprocess
import socket

"""
Search PATH for executable files with given name.

filename : string
result : list
"""
def which(filename, flags=os.X_OK):
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path == None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, filename)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result

'''
Get datetime of now
'''
def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

'''
Do process cmd
'''
def do_process(program):
    response = None

    try:
        response = subprocess.check_output(program,stderr=subprocess.STDOUT).split("\n")
    except subprocess.CalledProcessError,e:
        response = None
    finally:
        return response

'''
Get local ip address.
'''
def get_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

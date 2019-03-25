#!/usr/bin/python

import os
import time
import subprocess

from env import *
from misc import *

NTP_DATA_PATH_CMD = "/usr/sbin/ntpdate"

PKILL_CMD = "pkill -ef "

def kill_old_ntp_process():
    output, error, code = subprocess_open(PKILL_CMD + "req_ntp_server.py")
    if code == 0:
	print(output)
    else:
	print("not such old ntp process")

if __name__ == "__main__":
    
    if not os.path.exists(NTP_DATA_PATH_CMD):
	print("** not found ntpdate **")
	exit(-1)

    #check /etc/default/ntpdate ?
    
    kill_old_ntp_process()
    os.system("./req_ntp_server.py &") 
        

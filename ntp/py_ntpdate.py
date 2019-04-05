#!/usr/bin/python

import os
import sys
import time
import subprocess

from env import *
from misc import *

NTP_DATA_PATH_CMD = "/usr/sbin/ntpdate"

PKILL_CMD = "pkill -ef "
PGREP_CMD = "pgrep "

def kill_old_ntp_process():
    output, error, code = subprocess_open(PKILL_CMD + "req_ntp_server.py")
    print("** Completed killing old ntp processes **")

if __name__ == "__main__":
    if not os.path.exists(NTP_DATA_PATH_CMD):
	print("** not found ntpdate **")
	exit(-1)
    
    try:
	command = sys.argv[1]
    except IndexError:
	print("The command was not entered. Please re-enter the command")
	exit(-1)

    if command == "start":
	output, error, code = subprocess_open(PGREP_CMD + "req_ntp_server")
	if output and code == 0:
	    print("** The ntp process is already running **")
	else:
	    os.system("./req_ntp_server.py &")

    elif command == "stop":
	kill_old_ntp_process()

    elif command == "restart":
	print("** Restart ntpdate **")
	kill_old_ntp_process()
	os.system("./req_ntp_server.py &") 

    else:
	print(command +" is Invalid command")

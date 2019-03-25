#!/usr/bin/python

import os
import sys

from time import sleep
from env import *
from misc import *

NTP_CMD = 'ntp'

NTP_DATE_CMD = 'ntpdate '
MAX_RETRY_COUNT = 3
FIVE_MINUTE = 300

def request_ntp_server(ntp_domain):
    output, error, code = subprocess_open(NTP_DATE_CMD + ntp_domain)
    if not code == 0:
	return simple_error_response(code, error, RETURN_OPTION)
    else:
	return True

def sync_time_ntp_server(ntp_domain): 
    try_count = 0
    flag = False

    while(flag != True and try_count < MAX_RETRY_COUNT):
	flag = request_ntp_server(ntp_domain)
	print("request " + ntp_domain + " try_count = " + str(try_count) + " result = " + str(flag))
	if flag == True:
	    break
	else:
	    try_count +=1
	    #TO-DO, SNMP Trap Generate
	    sleep(FIVE_MINUTE)
    return flag

if __name__ == "__main__":
    ntp_data = show_uci(SYSTEM_CMD, NTP_CMD)
    try:
        activate = ntp_data['activate']
        poling_rate = int(ntp_data['poling'])*60
	ntp0_domain = ntp_data['serverdomain0']
    	ntp1_domain = ntp_data['serverdomain1']
    except:
        print("**System Ntp uci information is unusaul**")
        sys.exit(-1)

    if not activate == "1":
	print("ntp is not activated")
	sys.exit(0)

    while(True):
	if not sync_time_ntp_server(ntp0_domain) == True:
	    sync_time_ntp_server(ntp1_domain)
	sleep(poling_rate)

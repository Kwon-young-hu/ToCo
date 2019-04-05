#!/usr/bin/env python

import os
import sys
import subprocess

from env import *
from misc import *

FW_PRINTENV_ACTIVE_PART = 'fw_printenv active_part'
FW_SETENV = 'fw_setenv'
ACTIVE_PART = 'active_part'

UCI_SHOW_CMD = 'uci show '
UCI_GET_CMD = 'uci get '

EQUAL_DELIMITER = '='

TFTP_GET_CMD = 'tftp -g -r '

PATH_DEV_MTD3 = '/dev/mtd3 '
PATH_DEV_MTD2 = '/dev/mtd2 '

FLASH_ERASE = 'flash_erase '
NAND_WRITE = 'nandwrite '

EXIT_OPTION = '0'
RETURN_OPTION = '1'

def subprocess_open(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    returncode = popen.poll()
    return stdoutdata, stderrdata, returncode

def simple_error_response(code, error,end_option=EXIT_OPTION):
    print('An invalid result code was returned (error code: ' + str(code) + ')')
    print('Error message : ' + str(error))
    if end_option = RETURN_OPTION:
	return None
    else:
	sys.exit(-1)
    
def get_uci(conf_file, conf_section, conf_option):
    uci_cmd = '.'.join([conf_file, conf_section, conf_option])
    output, error, code = subprocess_open(UCI_GET_CMD + uci_cmd)
    if not code == 0:
	return simple_error_response(code, error, RETURN_OPTION)

    if '\n' in output:
	output = output.replace('\n','')
    return output
    
def get_os_image_from_tftp(file_name, server_addr):
    os.chdir("/tmp")
    print(TFTP_GET_CMD + file_name + ' ' + server_addr)
    output, error, code = subprocess_open(TFTP_GET_CMD + file_name + ' ' + server_addr)
    if not code == 0:
	return simple_error_response(code, error)

class ConfigNand:
    '''
    Write of Erase nand area
    '''
    def __init__(self, part_num):
	if part_num == '0':
	    self.conf_part = PATH_DEV_MTD3
	elif part_num == '1':
	    self.conf_part = PATH_DEV_MTD2
	else:
	    return None

    def erase(self):
	print(FLASH_ERASE + self.conf_part + '0 0')
	#output, error, code = subprocess_open(FLASH_ERASE + self.conf_part + '0 0')
	if not code == 0:
	    return simple_error_response(code,error)

    def write(self,img):
	if os.path.exists(img):
	    print(NAND_WRITE + self.conf_part + '-p ' + img)
	    #output, error, code = subprocess_open(NAND_WRITE + self.conf_part + '-p ' + img)

class ConfigEnv:
    '''
    active_part=0 ==> mtd2 used
    active_part=1 ==> mtd3 used
    '''
    def get_active_part(self):
	output, error, code = subprocess_open(FW_PRINTENV_ACTIVE_PART)
	if not code == 0:
	    return simple_error_response(code, error)
	else:
	    part_num = output.split('=')[1].replace('\n','')
	    return part_num

    def set_active_part(self, part_num):
	'''
	fw_setenv active_part 1 or 0
	'''
	active_part = ' '.join([FW_SETENV, ACTIVE_PART, part_num])
	print(active_part)
	output, error, code = subprocess_open(active_part)
	if not code == 0:
	    return simple_error_response(code, error)


if __name__ == "__main__":

    file_name = get_uci('system', 'upgrade','filename')
    server_ip = get_uci('system', 'upgrade','server')
    upgrade_type = get_uci('system', 'upgrade','type')
   
    if not file_name or server_ip or upgrade_type:
	print('**System upgrade uci information is unusual**')
	sys.exit(-1)

    if upgrade_type == '1':
	tftp_img = get_os_image_from_tftp(file_name, server_ip)
	    
	env_config = ConfigEnv()
	part_num = env_config.get_active_part()

	nand_config = ConfigNand(part_num)
	nand_config.erase()
	nand_config.write(file_name)

	if part_num == '0':
	    result = env_config.set_active_part('1')

	elif part_num == '1':
	    result = env_config.set_active_part('0')

	print('*** Firmware Upgrade finish! ***')
    
    elif upgrade_type == '0':
	print('To-Do...')




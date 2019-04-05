import os
import sys
import subprocess

from env import *

def subprocess_open(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    returncode = popen.poll()
    return stdoutdata, stderrdata, returncode

def simple_error_response(code, error,end_option=EXIT_OPTION):
    print('An invalid result code was returned (error code: ' + str(code) + ')')
    print('Error message : ' + str(error))
    if end_option == RETURN_OPTION:
        return None
    else:
        sys.exit(-1)

def dequote(s):
    if(s[0] == s[-1]) and s.startswith(("'",'"')):
        return s[1:-1]
    return s

def list_to_dict(data, delimiter):
    data_dict = dict()
    lines = data.splitlines()
    
    for line in lines:
        tokens = line.split(delimiter)
        data_dict[tokens[0]] = tokens[1]

    return data_dict
 

'''
UCI Config
'''
def get_uci(conf_file, conf_section, conf_option):
    uci_cmd = '.'.join([conf_file, conf_section, conf_option])
    output, error, code = subprocess_open(UCI_GET_CMD + uci_cmd)
    if not code == 0:
        return simple_error_response(code, error, RETURN_OPTION)

    if '\n' in output:
        output = output.replace('\n','')
    return output

def show_uci(conf_file, conf_section):
    uci_data = dict()
    conf_section = '.' + conf_section

    output, error, code = subprocess_open(UCI_SHOW_CMD + conf_file + conf_section)
    if not code == 0:
	return simple_error_response(code, error, RETURN_OPTION)

    data = list_to_dict(output, EQUAL_DELIMITER)
    for key, val in data.items():
        uci_str = conf_file + conf_section + '.'

        if uci_str in key:
            uci_key = key.replace(uci_str,'')
            uci_data[uci_key] = dequote(val)
    
    return uci_data
    

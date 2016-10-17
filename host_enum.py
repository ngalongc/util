#!/home/scan/venv/bin/python
import sys
import os
import subprocess

def run_cmd(cmd):
    subprocess.call(cmd,shell=True)


target = sys.argv[1]
subbrute_result_location = target + "_subbrute_result"
host_result_location = target + "_host_result"
def start_host(target):
    if os.path.isfile(subbrute_result_location):
        with open(subbrute_result_location,'r') as f:
            for hostname in f.readlines():
                hostname = hostname.strip()
                if hostname:
                    run_cmd("host "+hostname +">> {0}".format(host_result_location))
                else:
                    print debug_print("Please go back and run option 2 first")

start_host(target)

#!/home/scan/venv/bin/python
import sys
import subprocess
import os.path

def info_print(output):
    return "[*] " + output

def debug_print(output):
    return "[-] " + output

def found_print(output):
    return "[+] " + output


def help():
    print info_print("Usage: {0} example.com 1".format(sys.argv[0]))
    print info_print("Flag 1 : Automate all the process through 2-4")
    print info_print("Flag 2 : Just do sublist3r")
    print info_print("Flag 3 : Just do host")
    print info_print("Flag 4 : Just do result analysis")
    print info_print("Flag 5 : Just do nmap port scan")

    sys.exit(1)

if len(sys.argv) != 3:
    help()

option = int(sys.argv[2])
target = sys.argv[1]
relative_path_output_dir = "{0}".format(target)
subbrute_result_location = "{0}/{1}_subbrute_result".format(relative_path_output_dir,target)
host_result_location= relative_path_output_dir+"/"+target+"_host_lookup_result"
unique_hostname_location = relative_path_output_dir + "/" + target + "_unique_hostname_result"
unique_ip_location = relative_path_output_dir + "/" + target + "_unique_ip_result"


def run_cmd(cmd):
    subprocess.call(cmd,shell=True)


def start_subbrute(target):
    run_cmd("mkdir -p {0}".format(relative_path_output_dir))
    run_cmd("sublist3r -d {0} -t 20 -p80,443 -o {1}".format(target,subbrute_result_location)) # rmb to add subbrute to exe path /usr/local/bin


def start_host(target):
    if os.path.isfile(subbrute_result_location):
        with open(subbrute_result_location,'r') as f:
            for hostname in f.readlines():
                hostname = hostname.strip()
                if hostname:
                    run_cmd("host "+hostname +">> {0}".format(host_result_location))
                else:
                    print debug_print("Please go back and run option 2 first")

def start_analysis(target):
    if os.path.isfile(host_result_location):
        with open(host_result_location,'r') as f:
            hostname_list = []
            ip_address_list = []
            for line in f.readlines():
                if 'alias' in line:
                    alias_result = line.split('for')[1].strip().strip('.')
                    alias_original = line.split('is')[0].strip().strip('.')
                    hostname_list.append(alias_result)
                    hostname_list.append(alias_original)
                if 'address' in line:
                    ip_address = line.split('address')[1].strip()
                    ip_address_list.append(ip_address)
                    name = line.split('has')[0].strip()
                    hostname_list.append(name)
            #return a list of unique hostname found
            for i in list(set(hostname_list)):
                print found_print("Unique hostname found " + i)
            for i in list(set(ip_address_list)):
                print found_print("Unique IP found " + i)
            with open(unique_hostname_location, 'w+') as f:
                for i in list(set(hostname_list)):
                    f.write(i+"\n")
            with open(unique_ip_location, 'w+') as f:
                for i in list(set(ip_address_list)):
                    f.write(i+"\n")

    else:
        print debug_print("Please go back and run option 3 first")

def main():
    if option == 2:
        #Start subbrute first
        print info_print("Start subbrute now")
        start_subbrute(target)
        print info_print("Subbrute finish")
    if option == 3:
        # Do dnsrecon base on subbrute result
        print info_print("Start host lookup")
        start_host(target)
        print info_print("host command finish")

    if option == 4:
        # Do host command output analysis
        # Mainly process out the unique ip of the result, and see the collection of valid subdomain names
        print info_print("Start result analysis")
        start_analysis(target)
        print info_print("Result analysis finish")
main()

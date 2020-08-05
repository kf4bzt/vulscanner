#!/bin/python
# Vulnerabilty Scanner using NMAP and the Vulscan file suite to assess current Network security footprint.
# Download http://www.computec.ch/projekte/vulscan/?s=download and place vulscan directory files in the /usr/share/nmap/scripts location

import subprocess
import sys
import datetime
import time
import os
from _ast import List

working_dir = os.path.expanduser('~/vulscanner/')
if not os.path.exists(working_dir):
    os.makedirs(working_dir)

# Check for proper file and directorys
subnet_list = working_dir + 'subnet_list.txt'
vulscan_results = working_dir + 'vulscan_results_'
scan_results = working_dir + 'scan_results_'

# If the file subnet_list does not exist in the working_dir location, the user will be prompted
# to create one before the script will run. The file will need to be located in the path
# working_dir
#
if not os.path.isfile(subnet_list):
    print ("Please create subnet list called subnet_list.txt with one subnet/host per line in: " + working_dir)
    exit()

# If the file vulscan.nse does not exist in the working_dir location, the user will be prompted
# to create one before the script will run. The file will need to be located in the path
# /usr/share/nmap/scripts/vulscan/
#
if not os.path.isfile("/usr/share/nmap/scripts/vulscan/vulscan.nse"):
    print ("Please be sure nmap is installed and you have the vulscan files in /usr/share/nmap/scripts/vulscan dir")
    exit()

# Make a choice using the menu structure and place code under each choice
loop = 1
while loop == 1:

    # Clear Timestamps from filenames
    subnet_list = working_dir + 'subnet_list.txt'
    vulscan_results = working_dir + 'vulscan_results_'
    scan_results = working_dir + 'scan_results_'

    # Display simple menu with scanning options and use choice to select option
    print("Welcome to the Network Vulnerability Scanner")
    print()
    print("1) Single Port Scan")
    print("2) Multiple Subnet Port Scan")
    print("3) Multiple Subnet Vulnerability / Port Scan")
    print("4) Exit")
    print()

    # Define a function to open file and read in subnets file producing a space delimited list.
    # Format: One host or subnet per line.
    choice = input("Choose An Option: ")
    choice = int(choice)

    if choice == 1:
        print("Multiple subnet/hosts single port scan")
        port = input("Type a single port number: ")
        port = str(port)
        print("Scanning for port #: ") + port
        ts = time.time()
        fn_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
        scan_results += fn_timestamp

        with open(scan_results, 'w') as outfile:
            subprocess.call(['nmap', '-sT', '-p', port] + List(subnet_list), stdout=outfile)
        print("Scan complete, check results file: ") + scan_results
        outfile.close()
        print()

    elif choice == 2:
        print("Multiple subnet/hosts port scan in progress...")

        ts = time.time()
        fn_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
        scan_results += fn_timestamp

        with open(scan_results, 'w') as outfile:
            subprocess.call(['nmap', '-sT', '-iL', subnet_list], stdout=outfile)
        print("Scan Complete, check results file: ") + scan_results
        outfile.close()

    elif choice == 3:
        print("Multiple subnet vulnerability scan in progress...")
        print()

        ts = time.time()
        fn_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
        vulscan_results += fn_timestamp

        with open(vulscan_results, 'w') as outfile:
            subprocess.call(['nmap', '-sV', '-script=vulscan/vulscan.nse', '-iL', subnet_list], stdout=outfile)
        print("Scan Complete, check results file: ") + vulscan_results
        outfile.close()

    elif choice == 4:
        loop = 0

    else:
        print("Please enter a choice from the menu: ")

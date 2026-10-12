#https://pypi.org/project/python-nmap/
#https://github.com/johanlundberg/python-nmap/blob/master/README.txt
#https://nmap.org/book/man.html
#to scan metasploitable 2 use -Pn -sT -sV --script vuln -T4
#pip install python-nmap
from fileinput import filename
from pathlib import Path
import os
import nmap
#FEATURES TO INCLUDE:
#list all arguments, give basic example of scripts, combiniation of nmap entries 

def user_interface(): #user interface function to get user input for target and port
    print("====NMAP Scanner====")
    print('Please use this prototype responsibly and only scan targets that you have permission to scan. We are not responsible for any illegal activity performed with this prototype.')
    target =input("\nPress enter target IP or website to scan:")
    port = input("\nPress enter port number to scan:")
    return target, port

def nmap_status(np_target): #function determines if target is up or down
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{np_target}", arguments="-sn") #-sn argument allows for a ping scan and does not scan ports

    for host in nm.all_hosts():
        print(f"\nChecking Status of {host}")
        print(f"\n{host} ({nm[host].hostname()}) is {nm[host].state()}")
    print(f"")
    return 0

def saving_results(raw_xml_output): #function saves results to a xml file
    filename= input("Please enter a filename to save the scan results:")
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / f"{filename}.xml"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(raw_xml_output)
    print(f"Scan results saved to {file_path}")
    return 0

def display_nmap_arguments():
    path = Path(__file__).resolve().parent / 'nmap_arguments.txt'
    with open(path,'r') as f:
        nmap_argument_list=f.read()
    print(nmap_argument_list)

def nmap_scanner(ns_target, ns_port): #function performs a nmap scan of the target
    print("====Arguments====")
    print("List of common nmap arguments:")
    print("\n-sV: Version detection")
    print("\n-sS: TCP SYN scan")
    print("\n-sU: UDP scan")
    print("\n-sO: IP protocol scan")
    print("\n====Scripts====")
    
    display_nmap_arguments() #displays nmap commands, examples, and scripts
    
    ns_arguments = input("\nEnter nmap arguments to use for scan (default is -sV): ")
    print(f"\n====Scan Initiated====")
    
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{ns_target}", ports=f"{ns_port}", arguments=f"{ns_arguments}")
    
    for host in nm.all_hosts():
        print(f"\nScanning {host} on port {ns_port}")
        print(f"\n{host} ({nm[host].hostname()}) is {nm[host].state()}")
        for proto in nm[host].all_protocols():
            for port in sorted(nm[host][proto].keys()):
                info = nm[host][proto][port]
                print(f"{proto}/{port}: {info['state']} {info['name']} {info['product']} {info['version']}")
   

    choice =input("===== Saving Results ===== \n Would you like to save the results? (enter 'yes' or 'no'): ")
    if choice == "yes":
        raw_xml_output = nm.get_nmap_last_output().decode("utf-8")
        saving_results(raw_xml_output)
    if choice == "no":
        print("Results are not saved")
    return 0   


def main(): #core function
    print ("====Welcome to the Prototype====")
    choice = "start"
    
    while choice != "exit": #while loop will keep program running until user exits
        choice = input("\nWould you like to start a scan? (type 'start' to begin or 'exit' to quit): ")
        
        if choice == "start":
            target, port= user_interface()
            print(f"Checking status of target: {target} on port: {port}")
            nmap_status(target)
            print(f"Preparing to scan target: {target} on port: {port}")
            nmap_scanner(target, port)
            
        if choice == "exit":
            print("Exiting program")
            break
        
        if choice != "start" and choice != "exit":
            print("Invalid input, enter 'start' or 'exit' to continue")
        

if __name__ == "__main__":
    main()
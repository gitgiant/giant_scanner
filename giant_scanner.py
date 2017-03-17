#!/usr/bin/env python
import socket
import sys
import threading

MAX_THREADS = 50
socket.setdefaulttimeout(.05)

class ScannerThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        try:
            # connect to the given host:port
            self.sd.connect((self.host, self.port))
            print("Host: " + self.host + "\tPort: " + str(self.port) + " open.")
            self.sd.close()
        except:
            # print("Port: " + str(self.port) + " closed")
            pass
        # TODO: Add stats


class portScanner:
    def __init__(self, lower, upper, host):
        self.lower = lower
        self.upper = upper
        self.host = host
        print("Starting port scanner.")
        try:
            socket.gethostbyname(self.host)
        except:
            print ("Target host " + self.host + "not found.")
            return
        self.scan(self.lower, self.upper, self.host)

    def scan(self, lower, upper, host):
        self.lower = lower
        while self.lower <= upper:
            while threading.activeCount() < MAX_THREADS:
                ScannerThread(host, self.lower).start()
                self.lower += 1


if __name__ == "__main__":
    while True:
        print("Please select from the following options:")
        print("[L]AN scan:\t\tScan a range of local IPs to see what is on your LAN.")
        print("[P]ort scan:\tScan a range of ports on a target to see open TCP/IP ports.")
        print("[S]weep scan:\tScan a specific port on a range of IPs to see what ports are open on your LAN.")
        print("[C]onfigure settings.")
        choice = input("[Q]uit.").lower()

        if choice== 'l':
            # TODO: Implement prebaked ranges of ips (/24, /20, /16), call port scan/sweep scan on resulting IPs
            print("Please specify range of IPs to scan:")
            IPrange = input
        elif choice == 'p':
            # TODO: Impement most used ports (short ~1024, medium ~5000, long ~25000), resulting statistics
            host = input("Please specify a target host: ")
            start = int(input("Please specify start of range of ports to scan: "))
            end = int(input("Please specify end of range of ports to scan: "))

            if(start >= end or start > 65535 or end > 65534):
                print("Invalid input.")
                break
            portScanner(start, end, host)
        elif choice == 's':
            # TODO: Implement calling sweep scan on a found port/ip range
            pass
        elif choice == 'c':
            pass
        elif choice == 'q':
            print("Exiting...")
            exit(1)
        else:
            print("Invalid input.")



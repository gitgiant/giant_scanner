#!/usr/bin/env python
import socket
import sys
import threading
import ipaddress
import gmplot
import os
import webbrowser

MAX_THREADS = 50


# socket.setdefaulttimeout(.05)

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


# TODO: add time statistics
class portScanner:
    def __init__(self, lower, upper, host):
        self.lower = lower
        self.upper = upper
        self.host = host
        print("Starting port scanner...")
        try:
            socket.gethostbyname(self.host)
        except:
            print("Target host " + self.host + "not found.")
            return
        self.scan(self.lower, self.upper, self.host)

    def scan(self, lower, upper, host):
        self.lower = lower
        while self.lower <= upper:
            while threading.activeCount() < MAX_THREADS:
                ScannerThread(host, self.lower).start()
                self.lower += 1


class portListener:
    def __init__(self, port):
        self.port = port
        self.address = ''
        self.listen(self.port, self.address)
    #TODO: reset socket deafult timeout to a long time to listen
    def listen(self, port, address):
        addressList = []
        #loop forever until keyboard interrupt
        try:
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('127.0.0.1', port))
                s.listen(1)
                connection, address = s.accept()
                print("Established connection with: ", address)
                addressList.append(address[0])
                s.shutdown()
                s.close()
        except KeyboardInterrupt:
            print("Interrupted!")
            for address in addressList:
                print(address)


def is_port_invalid(port):
    if (port > 0 and port <= 65535):
        return False
    else:
        return True


if __name__ == "__main__":
    while True:
        print("Please select from the following options:")
        print("[I]P scan:\t\tScan a range of IPs.")
        print("[P]ort scan:\tScan a range of ports on a target IP to see open TCP/IP ports.")
        print("[S]weep scan:\tScan a specific port on a range of IPs.")
        print("[L]isten:\t\tListen on a port and generate reports based on attempted connections.")
        print("[O]ptions")
        print("[Q]uit")
        choice = input().lower()

        if choice == 'i':
            # TODO: Implement prebaked ranges of ips (/24, /20, /16), call port scan/sweep scan on resulting IPs
            inputIP = input("Please specify start of range of IPs to scan:")
            try:
                IPrange = ipaddress.ip_address(inputIP)
                print(IPrange)

            except:
                print("That is not a valid IP address.")
                break
                # TODO fire port scanner with range of host

        elif choice == 'p':
            # TODO: Impement most used ports (short ~1024, medium ~5000, long ~25000), resulting statistics
            host = input("Please specify a target host: ")
            if (host == 'localhost'):
                # make it place nice with ipaddress
                host = '127.0.0.1'
            try:
                IPhost = ipaddress.ip_address(host)
            except Exception as e:
                print(e)
                continue
            if (IPhost.is_global):
                print("Target host is a global IP. Scan will take much longer.")
                socket.setdefaulttimeout(1)
            else:
                print("Target host is a private IP.")
                socket.setdefaulttimeout(.05)
            try:
                start = int(input("Please specify start of range of ports to scan: "))
                end = int(input("Please specify end of range of ports to scan: "))
            except ValueError:
                print("Invalid input, please enter an integer for port")
                continue
            if (start > end or is_port_invalid(start) or is_port_invalid(end)):
                print("Invalid input.")
                break
            portScanner(start, end, host)

        elif choice == 's':
            # TODO: Implement calling sweep scan on a found port/ip range
            pass

        elif choice == 'l':
            port = int(input("Please specify the port to listen to: "))
            if (is_port_invalid(port)):
                print("Port is invalid")
                break
            print('Starting port listener on port {}.  Press Ctrl + C to interrupt'.format(port))

            portListener(port)

            # gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
            # gmap.draw("mymap.html")
            # webbrowser.open_new_tab('mymap.html')

        elif choice == 'o':
            pass
        elif choice == 'q':
            print("Exiting...")
            exit(1)
        else:
            print("Invalid input.")

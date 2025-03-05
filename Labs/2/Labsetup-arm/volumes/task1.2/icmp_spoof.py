#!/usr/bin/env python3
from scapy.all import *
import sys

if(len(sys.argv) != 3):
    print("Usage: %s <source_ip> <destination_ip>" % sys.argv[0])
    sys.exit(1)

src_ip = sys.argv[1]
dst_ip = sys.argv[2]

ip = IP()
ip.src = src_ip
ip.dst = dst_ip

icmp = ICMP()

packet = ip/icmp

print(f"Sending spoofed ICMP packet from {src_ip} to {dst_ip}")
packet.show()

send(packet, verbose=1)

print("Packet sent! Check packet capture to see the response.")

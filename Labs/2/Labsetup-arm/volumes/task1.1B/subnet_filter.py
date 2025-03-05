#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    print(f"[*] Subnet Packet captured:")
    pkt.show()

print("[*] Starting packet capture for subnet 128.230.0.0/16...")
pkt = sniff(iface='br-135b65d693d3', filter='net 128.230.0.0/16', prn=print_pkt, count=5)
print("[*] Capture complete")

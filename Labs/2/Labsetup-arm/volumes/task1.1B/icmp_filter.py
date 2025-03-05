#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    print(f"[*] ICMP Packet captured:")
    pkt.show()

print("[*] Starting ICMP packet capture...")

pkt = sniff(iface='br-135b65d693d3', filter='icmp', prn=print_pkt, count=10)
print("[*] Capture complete")

#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    print(f"[*] TCP Packet captured:")
    pkt.show()

print("[*] Starting TCP packet capture for specific source and port 23...")
pkt = sniff(iface='br-135b65d693d3', filter='tcp and src host 10.9.0.5 and dst port 23', prn=print_pkt, count=5)
print("[*] Capture complete")

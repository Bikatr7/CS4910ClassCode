#!/usr/bin/env python3
from scapy.all import *

def packet_callback(packet):
    print(f"[*] Captured packet: {packet.summary()}")

iface = "br-135b65d693d3"
print(f"[*] Starting sniffing on {iface}...")

sniff(iface=iface, prn=packet_callback, store=0)

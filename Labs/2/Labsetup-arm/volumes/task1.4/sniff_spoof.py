#!/usr/bin/env python3
from scapy.all import *

def spoof_icmp_reply(pkt):
    if(pkt.haslayer(ICMP) and pkt[ICMP].type == 8):
        print(f"[*] Detected ICMP Echo Request: {pkt[IP].src} -> {pkt[IP].dst}")
        
        ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
        icmp = ICMP(type=0, code=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)

        if(pkt.haslayer(Raw)):
            data = pkt[Raw].load
            reply = ip / icmp / data
        else:
            reply = ip / icmp
        
        print(f"[*] Spoofing ICMP Echo Reply: {pkt[IP].dst} -> {pkt[IP].src}")
        send(reply, verbose=0)

print("[*] Starting ICMP Sniff and Spoof program...")
print("[*] Monitoring for ICMP Echo Requests...")
sniff(filter="icmp", prn=spoof_icmp_reply, iface="br-135b65d693d3")
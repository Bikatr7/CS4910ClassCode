#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    pkt.show()

pkt = sniff(iface='br-135b65d693d3', filter='icmp', prn=print_pkt)

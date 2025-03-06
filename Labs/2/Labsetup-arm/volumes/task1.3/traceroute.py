#!/usr/bin/env python3
from scapy.all import *
import sys
import time

def traceroute(destination, max_hops=30, timeout=2):
    """
    Perform a traceroute to the destination.
    
    Args:
        destination: Target IP address or hostname
        max_hops: Maximum number of hops to try
        timeout: Timeout in seconds for each probe
    """
    print(f"\nStarting traceroute to {destination} (max {max_hops} hops)")
    print("=" * 60)
    print(f"{'TTL':<5} {'IP Address':<20} {'RTT (ms)':<10} {'Response Type'}")
    print("-" * 60)
    
    for ttl in range(1, max_hops + 1):
        packet = IP(dst=destination, ttl=ttl) / ICMP()
        
        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=0)
        rtt = (time.time() - start_time) * 1000
        
        if(reply is None):
            print(f"{ttl:<5} {'*':<20} {'timeout':<10}")
            if(ttl > 5 and ttl % 5 == 0):
                print(f"Multiple timeouts detected. Destination may be unreachable.")
                choice = input("Continue tracing? (y/n): ")
                if(choice.lower() != 'y'):
                    break
            continue
            
        if(reply.haslayer(ICMP)):
            icmp_type = reply.getlayer(ICMP).type
            icmp_code = reply.getlayer(ICMP).code
            
            if(icmp_type == 0):
                print(f"{ttl:<5} {reply.src:<20} {rtt:.2f} ms    Echo Reply (Destination reached)")
                print(f"\nDestination {destination} reached after {ttl} hops!")
                break
                
            elif(icmp_type == 11 and icmp_code == 0):
                print(f"{ttl:<5} {reply.src:<20} {rtt:.2f} ms    Time Exceeded")
                
            else:
                print(f"{ttl:<5} {reply.src:<20} {rtt:.2f} ms    ICMP type: {icmp_type}, code: {icmp_code}")
        else:
            print(f"{ttl:<5} {reply.src:<20} {rtt:.2f} ms    Non-ICMP Response")
    
    print("=" * 60)
    return

if(__name__ == "__main__"):
    if(len(sys.argv) != 2):
        print(f"Usage: {sys.argv[0]} <destination>")
        sys.exit(1)
        
    destination = sys.argv[1]
    traceroute(destination)

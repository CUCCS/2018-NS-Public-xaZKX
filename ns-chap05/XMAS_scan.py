import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "192.168.56.104"
src_port = RandShort()
dst_port = 80

pkt = IP(dst=dst_ip) / TCP(dport=dst_port, flags="FPU")

xmas_scan_resp = sr1(pkt, timeout=10)
if (str(type(xmas_scan_resp)) == "<type 'NoneType'>"):
    print("Open|Filtered")
elif (xmas_scan_resp.haslayer(TCP)):
    if (xmas_scan_resp.getlayer(TCP).flags == 0x14):
        print("Closed")
elif (xmas_scan_resp.haslayer(ICMP)):
    if (int(xmas_scan_resp.getlayer(ICMP).type) == 3 and int(xmas_scan_resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
        print("Filtered")

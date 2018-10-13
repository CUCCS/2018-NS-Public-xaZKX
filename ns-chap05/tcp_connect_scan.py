import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
dst_ip = "192.168.56.104"
src_port = RandShort()
dst_port = 80

pkt = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S")
pkt1 = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="AR")
tcp_connect_scan_resp = sr1(pkt, timeout=10)

if (str(type(tcp_connect_scan_resp)) == "<type 'NoneType'>"):
    print("Closed")
elif (tcp_connect_scan_resp.haslayer(TCP)):
    if (tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
        send_rst = sr(pkt1, timeout=10)
        print("Open")
    elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
        print("Closed")

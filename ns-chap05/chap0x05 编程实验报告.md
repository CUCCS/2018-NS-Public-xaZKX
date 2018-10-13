## TCP connect scan

- 实现原理：
  - connect（）
  - 完成TCP三次握手

![](C:/ns-chap05/images/tcp_cs1.png)

![](C:/ns-chap05/images/tcp_cs2.png)

- 编程实现（tcp_connect_scan.py）

```python
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

```
- 在Attacker上运行此文件。并在Vitcim中监听，将收到的包存进cap文件中。

![](C:/ns-chap05/images/tcs_a.png)

![](C:/ns-chap05/images/tss_w.png)

- 可以看到输出为“*Closed*”，并且监听到的包只有SIN包和RST包，说明Vitcim的80端口是关闭状态。

- 在Vitcim中监听80端口后，重新发包。

``` 
ns -ls 80
```

![](C:/ns-chap05/images/tcs_aa.png)

![](C:/ns-chap05/images/tcs_ww.png)

- 可以看到输出为“*Open*”，并且完成了三次握手。

## TCP stealth scan

- 实现原理：

![](C:/ns-chap05/images/ts_scan1.png)

![](C:/ns-chap05/images/tcp_cs2.png)

- 编程实现（stealth_scan.py）

```python
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "192.168.56.104"
src_port = RandShort()
dst_port = 80

pkt = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S")
pkt1 = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="R")

stealth_scan_resp = sr1(pkt, timeout=10)

if (str(type(stealth_scan_resp)) == "<type 'NoneType'>"):
    print("Filtered")
elif (stealth_scan_resp.haslayer(TCP)):
    if (stealth_scan_resp.getlayer(TCP).flags == 0x12):
        send_rst = sr(pkt1, timeout=10)
        print("Open")
    elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
        print("Closed")
elif (stealth_scan_resp.haslayer(ICMP)):
    if (int(stealth_scan_resp.getlayer(ICMP).type) == 3 and int(stealth_scan_resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
        print("Filtered")

```
- 在Attacker上运行此文件。并在Vitcim中监听，将收到的包存进cap文件中。

![](C:/ns-chap05/images/tss_a.png)

![](C:/ns-chap05/images/tss_w.png)

- 可以看到输出为“*Closed*”，并且监听到的包只有SIN包和RST包，说明Vitcim的80端口是关闭状态。


- 在Vitcim中监听80端口后，重新发包。

``` 
ns -ls 80
```

![](C:/ns-chap05/images/tss__aa.png)

![](C:/ns-chap05/images/tss_ww.png)

- 可以看到输出为“*Open*”。

## TCP XMAS scan
 - 实现原理：设置TCP报文头FIN、URG和PUSH标记

![](C:/ns-chap05/images/tx_scan1.png)

![](C:/ns-chap05/images/tx_scan2.png)

![](C:/ns-chap05/images/tx_scan3.png)


- 编程实现（stealth_scan.py）


```python
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

```
- 在Attacker上运行此文件。并在Vitcim中监听，将收到的包存进cap文件中。

![](C:/ns-chap05/images/txs_aa.png)

![](C:/ns-chap05/images/txs_ww.png)

- 可以看到输出为“*Closed*”，并且监听到的包只有SIN包和RST包，说明Vitcim的80端口是关闭状态。

- 在Vitcim中监听80端口后，重新发包。

``` 
nc -lp 80
```


![](C:/ns-chap05/images/txs_a.png)

![](C:/ns-chap05/images/txs_w.png)

- 可以看到输出为“*Open|Filtered*”，并且只有攻击者发送的一个UDP包，没有任何回复。

## UDP scan

- 实现原理：

![](C:/ns-chap05/images/UDP.png)

![](C:/ns-chap05/images/UDP2.png)

![](C:/ns-chap05/images/UDP3.png)

- 编程实现（UDP_scan.py）


```python
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "192.168.56.104"
src_port = RandShort()
dst_port = 53
dst_timeout = 10

udp_scan_resp = sr1(IP(dst=dst_ip) / UDP(dport=dst_port), timeout=dst_timeout)
if (str(type(udp_scan_resp)) == "<type 'NoneType'>"):
    print("Open|Filtered")
elif (udp_scan_resp.haslayer(UDP)):
    print("Open")
elif (udp_scan_resp.haslayer(ICMP)):
    if (int(udp_scan_resp.getlayer(ICMP).type) == 3 and int(udp_scan_resp.getlayer(ICMP).code) == 3):
        print("Closed")
    elif (int(udp_scan_resp.getlayer(ICMP).type) == 3 and int(udp_scan_resp.getlayer(ICMP).code) in [1, 2, 9, 10, 13]):
        print("Filtered")

```

- 在Attacker上运行此文件。并在Vitcim中监听，将收到的包存进cap文件中。

![](C:/ns-chap05/images/udp_aa.png)

![](C:/ns-chap05/images/udp_ww.png)

- 可以看到输出为“*Closed*”,并且有一个UDP包和一个ICMP Error(Type 3, Code 3),说明Vitcim的53端口是关闭状态。


- 在Vitcim上监听53端口后，重新发包。

``` 
ns -ulp 53 
```
![](C:/ns-chap05/images/udp_a.png)

![](C:/ns-chap05/images/udp_w.png)

- 可以看到输出为“*Open/Filtered*”,并且只有攻击者发送的一个UDP包，没有任何回复。
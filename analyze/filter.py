from scapy.all import rdpcap,wrpcap,PacketList
from PcapAnalyze import get_http_payload

zh_pcaps = rdpcap('/Users/yg/code/Application-Traffic-Identification/data/zhihu/zhihu_req.pcap')
to_del = list()
print(len(zh_pcaps))
for i in range(len(zh_pcaps)):
    http_pld = get_http_payload(zh_pcaps[i])
    host = http_pld.Host
    if host.find(b'opera') != -1:
        print(i)
        print(host)
        to_del.append(i)

for i in range(len(to_del)+1):
    if i == 0:                  # the first value
        p1 = zh_pcaps[0: to_del[0]]
    elif i == len(to_del):    # the last value
        p1 += zh_pcaps[to_del[i-1]+1 : ]
    else:
        p1 += zh_pcaps[to_del[i-1]+1 : to_del[i]]

wrpcap("p1.pcap", p1)

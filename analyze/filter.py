from scapy.all import rdpcap,wrpcap
from PcapAnalyze import get_http_payload

zh_pcaps = rdpcap('/Users/yg/code/Application-Traffic-Identification/data/zhihu/zhihu_req.pcap')
to_del = list()
for i in range(len(zh_pcaps)):
    http_pld = get_http_payload(zh_pcaps[i])
    path = http_pld.Path
    if path.find(b'opera') != -1:
        print(i)
        print(path)
        to_del.append(i)

for i in range(len(to_del)):
    if i == 0:                  # the first value
        p1 = zh_pcaps[0: to_del[0]]
    elif i == len(to_del)-1:    # the last value
        p1 += zh_pcaps[to_del[i]+1 : ]
    else:
        p1 += zh_pcaps[to_del[i]+1 : to_del[i+1]]

wrpcap("p1.pcap", p1)

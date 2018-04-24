try:
    import scapy.all as scapy
except ImportError:
    import scapy

try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http


def delimiter():
    print('=' * 66)


def get_http_payload(ether):
    return ether.payload.payload.payload.payload

def analyze():

    packets = []
    """
    for i in range(1, 7):
        file = "/Users/yg/code/Application-Traffic-Identification/data/weibo_req"+str(i)+".pcap"
        pcaps = rdpcap(file)
        print(i, ": ", len(pcaps))
    """
    pcapFile_weibo = "/Users/yg/code/Application-Traffic-Identification/data/weibo_http_request.pcap"
    pcapFile_zhihu = "/Users/yg/code/Application-Traffic-Identification/p1.pcap"
    packets = scapy.rdpcap(pcapFile_zhihu)
    print("pcapFile has", len(packets), "packets.")
    packet = packets[0]
    # print(packet.time)
    print(len(packets))
    # packet[0].show()
    # print(packet['HTTP'].show())

    delimiter()
    for f in packet.fields_desc:
        pass
        # print(f)
    delimiter()

    ip_payload = packet.payload
    for f in ip_payload.fields_desc:
        pass
        # print(f)
    delimiter()

    tcp_payload = ip_payload.payload
    for f in tcp_payload.fields_desc:
        pass
        # print(f)
    delimiter()

    http_payload = tcp_payload.payload.payload
    fields_cnt = 0
    for f in http_payload.fields_desc:
        # print(f)
        fields_cnt += 1
    delimiter()

    print("http: fields_cnt = ", fields_cnt)
    # print(packet['HTTP Request'].summary())
    # packet.pdfdump(layer_shift=5)
    # packet.psdump("/tmp/http_get.eps", layer_shift=1)

    cnt_get = 0
    cnt_post = 0
    cnt_img = 0
    cnt_mp4 = 0
    cnt_sdkad = 0
    cnt_other = 0
    dc_host = dict()
    lens = list()
    fields_not_none = set()
    header_lens = list()

    pkt_num = len(packets)
    for i in range(pkt_num):
        http_payload = get_http_payload(packets[i])
        method = http_payload.Method
        path = http_payload.Path
        if method == b'GET':
            cnt_get += 1
        elif method == b'POST':
            cnt_post += 1

        if path.find(b'jpg') != -1 or path.find(b'png') != -1:
            cnt_img += 1
        elif path.find(b'mp4') != -1:
            cnt_mp4 += 1
        elif path.find(b'sdkad') != -1:
            cnt_sdkad += 1
        else:
            cnt_other += 1
            # print(http_payload.Path)

        host = http_payload.Host
        if host in dc_host:
            dc_host[host] += 1
        else:
            dc_host[host] = 1

        lens.append(len(http_payload))

        len_tmp=0
        for field in http_payload.fields_desc:
            val = http_payload.getfieldval(field.name)
            if val is not None:
                fields_not_none.add(field.name)
                len_tmp += len(val)
                header_lens.append(len_tmp)


    delimiter()
    print('get : ', cnt_get)
    print('post: ', cnt_post)
    delimiter()
    print('jpg: ', cnt_img)
    print('mp4: ', cnt_mp4)
    print('sdkad: ', cnt_sdkad)
    print('other: ', cnt_other)
    delimiter()
    sorted_keys = sorted(dc_host.keys())
    for host in sorted_keys:
        print('%s :\t%d' % (host, dc_host[host]))
    delimiter()
    print('average length: ', sum(lens)/len(lens))
    delimiter()
    print('', fields_not_none)
    delimiter()
    print('average header length: ', sum(header_lens)/len(header_lens))
    # print(packet.time)


if __name__=='__main__':
    analyze()
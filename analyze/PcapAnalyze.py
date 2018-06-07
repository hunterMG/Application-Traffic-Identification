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
    pcapFile_weibo = "../data/weibo_http_request.pcap"
    pcapFile_huafen = "../data/huafen_req.pcap"
    pcapFile_jianshu = "../data/jianshu_req.pcap"
    pcapFile_tieba = "../data/tieba_req.pcap"
    pcapFile_zhihu = "../data/zhihu/zhihu_req.pcap"
    packets = scapy.rdpcap(pcapFile_jianshu)
    output_txt = open('./jianshu.txt', 'w')    
    print("pcapFile has", len(packets), "packets.")
    packet = packets[0]
    # print(packet.time)
    # print(len(packets))
    # packet[0].show()
    print(type(packet['HTTP']))
    http_payload = get_http_payload(packet)
    print(type(http_payload))
    print(http_payload)
    print(http_payload == packet['HTTPRequest'])

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
    num_valid_pkt = 0
    char_summary = set()
    for i in range(pkt_num):
        http_payload = get_http_payload(packets[i])
        # 去除第三方SDK请求
        # if http_payload.getfieldval('Host') == b'sdk.open.phone.igexin.com':
        #     continue
        # 统计有效packet数量
        num_valid_pkt += 1
        method = http_payload.Method
        # 去掉post请求的payload
        http_payload.remove_payload()
        # 写入文件        
        try:
            tmp = str(bytes(http_payload), encoding='utf-8')
            for c in tmp:
                char_summary.add(c)
            output_txt.write(tmp)
        except UnicodeDecodeError:
            print('Error when decode packet : ', i)
        """
        if method == b'POST':
            # 提取首部
            all_bytes = bytes(http_payload)
            try:
                raw_bytes = bytes(http_payload['Raw'])
                header_bytes = all_bytes.rstrip(raw_bytes)
            except IndexError:
                header_bytes = all_bytes
        if i == 54:
            print(http_payload)
            http_payload.remove_payload()
            print(http_payload)
        try:
            if method == b'GET':
                tmp = str(bytes(http_payload), encoding='utf-8')
                output_txt.write(tmp) # 写入文件
            else:   # post
                tmp = str(header_bytes, encoding='utf-8')
                if tmp.endswith('\n') and not tmp.endswith('\n\n'):
                    tmp += '\n'
                elif not tmp.endswith('\n'):
                    tmp += '\n\n'
                output_txt.write(tmp)
        except UnicodeDecodeError:
            http_payload['Raw'].show()
            print(type(http_payload['Raw']))    
            if i < 6666:
                print('ERROR: i = ', i)
                print(http_payload.getfieldval('Accept-Encoding'), ' , ' , http_payload.getfieldval('Method'))
                print(http_payload)
                # http_payload.show()
        """
        # 统计字段
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
    print('有效的packet数量：', num_valid_pkt)
    print('字符统计：', char_summary)
    print('共有字符个数：', len(char_summary))

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

    output_txt.close()


if __name__=='__main__':
    analyze()
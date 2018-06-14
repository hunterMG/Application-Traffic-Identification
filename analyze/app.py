
# import os, sys

# try:
#     os.environ['LD_LIBRARY_PATH'] += '/usr/local/cuda-9.0/lib64:/usr/local/cuda/extras/CUPTI/lib64'
# except KeyError:
#     os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda-9.0/lib64:/usr/local/cuda/extras/CUPTI/lib64'

# try:
#     os.environ['PATH'] += '/usr/local/cuda-9.0/bin:/usr/local/cuda-9.0/lib64'
# except KeyError:
#     os.environ['PATH'] = '/usr/local/cuda-9.0/bin:/usr/local/cuda-9.0/lib64'
    
# print('888888888888888888888888888888888888888888888888888888')
# print(os.environ['LD_LIBRARY_PATH'])
# print(os.environ['PATH'])
# print('888888888888888888888888888888888888888888888888888888')

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

from numpy import argmax
import numpy as np
from keras.models import load_model
from keras.utils import np_utils


# 由原始的数据包提取HTTP包
def get_http_payload(ether):
    return ether.payload.payload.payload.payload

alphabet = ['+', ';', '%', 'r', '~', 'R', 'f', '}', 'n', 'u', 'N', 'L', '7', 'Z', '3', 'w', '!', '0', '6', 'm', 'E', ',', '[', '{', 'b', '?', 'j', 'U', 'S', 'q', '$', 'd', '\n', 's', 'T', '-', 'F', 'h', '\r', '8', 'g', '4', 'V', 'v', ']', 't', '2', 'a', 'z', 'c', '/', '.', '_', '*', 'K', 'Q', 'y', '(', 'x', 'W', 'Y', 'i', 'M', 'A', '@', '|', '5', ':', 'p', 'B', '9', 'H', 'J', ')', '"', '&', 'G', 'l', 'D', 'C', '1', ' ', 'P', 'O', 'I', 'e', 'k', 'o', '=', 'X']

char2int = dict((c, i) for (i, c) in enumerate(alphabet))
int2char = dict((i, c) for (i, c) in enumerate(alphabet))

def onehot_encode(data):
    """
        data: 需要编码的字符串
        return： 编码后的矩阵
    """
    integer_encoded = [char2int[char] for char in data] # 获得对data编码的list   
    onehot_encoded = list()
    for value in integer_encoded:
           letter = [0 for _ in range(len(alphabet))]   # 生成一个全0的list
           letter[value] = 1
           onehot_encoded.append(letter)
    return onehot_encoded
# 预处理
#   args：
#       http_payload ：去除载荷之后的HTTP包
#   return: 编码后的向量
def preprocess(http_payload):
    tmp = str(bytes(http_payload), encoding='utf-8')
    # 不足230个字符的以空格填充
    tmp = tmp.ljust(230, ' ')
    # 取前230个字符
    tmp = tmp[:230]
    encoded = onehot_encode(tmp)
    np_encoded = np.array(encoded)
    return np_encoded

def http_header(packet):
    # 获取HTTP包
    http_payload = get_http_payload(packet)
    # 去除HTTP包的载荷
    http_payload.remove_payload()
    
    if isinstance(http_payload, scapy_http.http.HTTPRequest) :
        print("\n***************************************GET PACKET****************************************************")
        print(http_payload.Method, http_payload.Host)
        # 预处理
        X_test = preprocess(http_payload)
        X_test = X_test.reshape(-1, 1, 230, 90)
        # predict
        res_array = model.predict(X_test, verbose=0)
        # print(res_array)
        res = np.argmax(res_array, 1)
        # print(res)
        if res == 0:
            print("分类结果： 微博")
        elif res == 1:
            print("分类结果： 知乎")
        elif res == 2:
            print("分类结果： 贴吧")
        elif res == 3:
            print("分类结果： 简书")
        elif res == 4:
            print("分类结果： 花粉")
        else:
            print("分类结果： 未知")
        print("*****************************************************************************************************")
        # for field in http_payload.fields_desc:
            # print(field.name)
        # return HTTP_print(http_payload)
        # return http_packet
def HTTP_print(packet1):
    ret = "***************************************GET PACKET****************************************************\n"
    # ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += str(packet1.Method) + ' ' + str(packet1.Host) + '\n'
    ret += "*****************************************************************************************************\n"
    return ret


if __name__ == "__main__":
    # env_fix()
    model = load_model('my_model1.h5')
    print('开始监听流量：')
    scapy.sniff(iface='en2', prn=http_header, filter="dst port 80", count=0)
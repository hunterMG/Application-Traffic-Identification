#!/home/yg/.local/share/virtualenvs/Application-Traffic-Identification-8Rjd059g/bin/python

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
import os

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

def pcap_to_X(pcapFile):
    pkts = scapy.rdpcap(pcapFile)
    X_tmp = np.empty((len(pkts), 230, 90))
    i = 0
    with scapy.PcapReader(pcapFile) as pcap_reader:
        for pkt in pcap_reader:
            http_payload = get_http_payload(pkt)
            http_payload.remove_payload()
            tmp = str(bytes(http_payload), encoding='utf-8')
            # 不足230个字符的以空格填充
            tmp = tmp.ljust(230, ' ')
            # 取前230个字符
            tmp = tmp[:230]
            encoded = onehot_encode(tmp)
            np_encoded = np.array(encoded)
            X_tmp[i] = np_encoded
            i += 1
        print(i)
    return X_tmp
pcap_file = '../data/test/huafen_test.pcap'
X = pcap_to_X(pcap_file)
full_name = os.path.split(pcap_file)[-1]
name = os.path.split(full_name)[0]
npy_file = name + '.npy'
np.save(npy_file, X)
# y = np.ones(100) * 4
# np.save('y_hf.npy', y)

# 从文件加载预训练好的模型及权重
model = load_model('my_model.h5')
# preprocess
X = X.reshape(-1, 1, 230, 90)
# predict
res_array = model.predict(X, verbose=1)
print(res_array)
res = np.argmax(res_array, 1)
print(res)
for i in res:
    if i != 4:
        print(i)
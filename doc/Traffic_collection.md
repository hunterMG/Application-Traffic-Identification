## [Charles Proxy](http://www.cnblogs.com/rrl92/p/7928770.html)
[Download](https://www.charlesproxy.com/latest-release/download.do)  

[crack](https://www.zzzmode.com/mytools/charles/),([Repository](https://github.com/8enet/Charles-Crack))  
Put the jar file generated in directory 'lib'(which is in Charles installation directory).

Configure: Proxy -> Proxy setting:
```
Port: 8888
Enable transparent HTTP proxying
```

## Genymotion
> In your Genymotion Android emulator…  
Settings -> Wifi -> Press and hold your active network  
Select “Modify Network”  
Select “Show Advanced Options”  
Select “Proxy Settings -> Manual”  
Set your Proxy to: 10.0.3.2 (Genymotion’s special code for the local workstation)  
Set your Port to: 8888(specified in Charles)  
Press Save  
You should now be able to see Genymotion traffic showing up in your Charles Proxy.[refer](http://rexstjohn.com/using-genymotion-charles-proxy/)

## HTTPS
Help -> SSL Proxying -> Install Charles Root Certificate on a Mobile Device  
In android web browser type 'chls.pro.ssl', install it.  
Proxy -> SSL Proxy Settings -> SSL Proxying:
```
Enable SSL Proxying
Add:
    Host: * (* means match all hosts)
    Prot: 443
```

## tcpdump
[A tcpdump Tutorial and Primer with Examples](https://danielmiessler.com/study/tcpdump/#basics)  
[tcpdump抓取HTTP包](https://blog.csdn.net/kofandlizi/article/details/8106841)  
[tcpdump只抓取HTTP报文头部](https://blog.csdn.net/lotluck/article/details/79797117)  

```sh
# 获取包名 (加 ‘-f’ 列出安装位置)
adb shell pm list packages
# 进入android terminal
adb shell
# 捕获流量
tcpdump -vv -s 0 -i eth1 -w /tmp/http.pcap -c 100 dst port 80 and tcp[20:2]=0x4745

tcpdump -vvnns 0 -i eth1 -w /tmp/weibo_req.pcap -c 1000 'dst port http and (tcp[20:2]=0x4745 or tcp[20:2]=0x504F)'


# 模拟事件
adb shell monkey -p com.sina.weibo -v 500 --throttle 120
# 复制文件到本地主机
adb pull /sdcard/android.pcap ./android.pcap

```
[Monkey](https://developer.android.com/studio/test/monkey.html)  
tcpdump 参数说明:  
>   -vv：获取详细的包信息（注意是两个 v 不是 w）  
    -s 0：不限数据包的长度，如果不加则只获取包头  
    -w xxx.pcap：捕获数据包名称以及存储位置（本例中保存在 sdcard 路径下，数据包名为 capture.pcap）  
    -i eth1：捕获制定的网卡（在 genymotion 虚拟机中，使用 busybox ifconfig 命令可以查看相关信息，一般 genymotion 的 ip 地址都为 10.xx.xx.x）  
    如果你想指定捕获的数据包数量，可以使用 -c 参数（例如 -c 128  ）
    捕获结束，直接按 Ctrl + C 即可  
    "GE": 0x4745, "HT": 0x4854, "PO": 0x504F   
    [ASCII码对照表](http://ascii.911cha.com/)

## Pcap Analisys
python module : `scapy`, `scapy-http`  
```sh
pipenv install scapy-python3 scapy-http pyx(optional)
brew install libdnet libpcap
brew cask install mactex # PyX dependency, for pdfdump(),psdump(), etc.
# pipenv install netifaces
```

## Package names
Weibo: com.sina.weibo  
zhihu: com.zhihu.android

## editcap, mergecap
[refer](https://www.linuxidc.com/Linux/2015-01/112471.htm)
```sh
# 默认将内部的数据包以时间先后来排序
mergecap -w output.pcap input.pcap input2.pcap [input3.pcap ...]
# 以命令行中的顺序来合并文件
mergecap -a -w output.pcap input.pcap input2.pcap

```

## remove the last corrupt packet
```python
from scapy.all import *

pcap = rdpcap('zhihu_req1.pcap')
p1 = pcap[0: len(pcap)-1]
wrpcap('p1.pcap', p1)
```

---
title: 如何下载S-net数据
categories:
  - work
tags:
  - seismic
abbrlink: 2bac6571
date: 2024-07-09 15:16:25
---
&emsp;&emsp;如何下载S-net数据呢？
<!--less-->
&emsp;&emsp;S-net是NIED（日本国立防灾科学技术研究所）布设的海底地震动观测网络，由150台三分量地震仪组成。观测区域覆盖了2011年东日本大地震及其邻近地区的震源区域。自2017年4月以来，S-net已全面开始运作，实时地将数据传回NIED。
&emsp;&emsp;如何下载S-net的数据呢？参见Seisman的[HinetPy](https://seisman.github.io/HinetPy/)。
### 安装
1. 用命令安装HinetPy，用python3.8以上版本，命令为。
```
python -m pip install HinetPy
```
2. 安装win32tools
在[hinet](https://hinetwww11.bosai.go.jp/auth/manual/?LANG=en)网站下载安装包[win32tools.tar.gz](https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools)，运行:
```bash
tar -xvf win32tools.tar.gz
cd win32tools/
make
```
把catwin32.src/catwin32和win2sac.src/win2sac_32拷贝到环境变量认识的位置。
### 运行
&emsp;&emsp;具体怎么下载数据自己去看说明就好了。我想要下载连续数据，所以写了个循环脚本，如下：
```
import os
from HinetPy import Client
from HinetPy import win32
from datetime import datetime,timedelta

client = Client ("xxxx","xxxx")
# 这里输入你自己的账号和密码。自己申请就好了。
endtime=datetime(2016,8,16,2,0) # 截至时间
time=datetime(2016,8,16,1,40)   # 开始时间
dt=timedelta(minutes=20)        # 时间增量（分钟记）
dir="data"                      # 数据存在dir下面
while (time<endtime):
    print(time,endtime)
    y="%04d"%time.year
    m="%02d"%time.month
    d="%02d"%time.day
    h="%02d"%time.hour
    mm="%02d"%time.minute
    name=y+"_"+m+"_"+d+"_"+h+"_"+mm+".cnt"
    cname=y+"_"+m+"_"+d+"_"+h+"_"+mm+".ch"
    outd=dir+"/"+y+"_"+m+"_"+d+"_"+h+"_"+mm #每20分钟一个文件夹
    data=dir+"/"+y+"_"+m+"_"+d+"_"+h+"_"+mm+".cnt"
    ctable=dir+"/"+y+"_"+m+"_"+d+"_"+h+"_"+mm+".ch"
    if not os.path.exists(ctable):
        # 如果仪器信息文件没有则创建一个空的，这样做可以多跑几个进程，同时下载，并保证不重复。
        with open(ctable, 'w') as file:
            pass
        dat,ctabl = client.get_continuous_waveform("0120",time,20,data=name,ctable=cname,outdir=dir) # 下载数据，这里0120就是指代S-net。client.info()可以查看所有台网。 outdir指定保存数据的文件夹。
        if os.access(data, os.F_OK):
        # 如果下载成功则进行解压。如果没有数据，强行进行解压，程序就出错跳出来。
        #if os.path.getsize(data) != 0:
            win32.extract_sac(data,ctable,outdir=outd) #解压sac。
            win32.extract_sacpz(ctable, outdir=outd) #解压仪器响应。
    time=time+dt
```
&emsp;&emsp;NEID下载数据有个限制就是道数X时间（按分钟记）<12000。S-net有150个台，三分量就是450道，因此12000/450=26.666分钟，即每次最长可下载不超过26分钟数据。为了方便我搞的是20分钟。
&emsp;&emsp;其他没有什么问题，就是下载数据好慢。

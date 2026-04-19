---
title: 如何下载Fnet数据
tags:
  - python
categories:
  - work
abbrlink: '98618e37'
date: 2025-04-22 08:36:57
---
感谢Seisman写了[FnetPy](https://github.com/seisman/FnetPy),可以很方便地下载数据。
安装：
```
pip install https://github.com/seisman/FnetPy/archive/master.zip
```
例子：
```
import os
from obspy.io.xseed import Parser
from FnetPy import Client
from datetime import datetime,timedelta
from obspy import read_inventory,read,Trace
from datetime import datetime
client = Client('用户名', '密码')

current_date=datetime(2013,1,1,0,0)
#current_date=datetime(2004,12,30,0,0)
end_date=datetime(2025,1,1,0,0)
output_dir='./seed'
raw_dir='./raw'
resp_dir='./resp'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(resp_dir, exist_ok=True)
while (current_date<end_date):
    start_time = current_data
    start_str = current_date.strftime("%Y_%m_%d_%H_%M_%S")
    name=start_str+".seed"
    fname=os.path.join(raw_dir,name)
    output_file=os.path.join(output_dir, name)
    if os.path.exists(output_file):
        print(f"[跳过] 文件已存在: {output_file}")
        current_date+=timedelta(days=1)
        continue
    open(output_file, 'wb').close()  # 创建空文件
    if not os.path.exists(fname):
        print('download data from '+str(start_time)+' to '+str(end_time))
        client.get_waveform(start_time, duration_in_seconds=86400+3600,component="LHZ",filename=fname) # download
        print('download '+fname+' down!')
    current_date+=timedelta(days=1)
    st = read(fname) # read
    parser = Parser(fname) #parse
    parser.write_resp(resp_dir, zipped=False)
    for tr in st:
        resp_file = f"RESP.{tr.get_id()}"
        inv = read_inventory(os.path.join(resp_dir, resp_file))
        tr.remove_response(inventory=inv, output="VEL")
        #print(tr.stats)
    st.write(output_file, format="MSEED")
print('Finished')
```
这个脚本可以下载2013到2025年Fnet所有台站的LHZ连续波形数据，数据长度为25小时，overlap 1小时。去除仪器响应后的速度记录存放在seed文件夹中。每天的数据名称为%Y_%m_%d_%H_%M_%S.seed。账户需要去NIED去申请，当然用我的也可以。

---
title: 如何下载Fnet的台站列表
categories:
  - work
tags:
  - web
abbrlink: f46e64ed
date: 2024-09-01 10:52:18
---
&emsp;&emsp;如何下载Fnet的台站列表？
<!--less-->
&emsp;&emsp;这里其实是一个网页抓取的工作。Fnet台站列表网址是https://www.fnet.bosai.go.jp/st_info/?LANG=en。那么下载其列表并保存到本地的python脚本如下：
```
import pandas as pd
import requests
url = 'https://www.fnet.bosai.go.jp/st_info/?LANG=en'
response = requests.get(url)
print(response.content)
dfs = pd.read_html(response.content)
if len(dfs) > 0:
    df = dfs[2]
    df.to_csv('fnet_station.csv',index=False)
    print("表格已保存为 fent_station.csv 文件。")
else:
    print("未找到表格。")
```
注意到保存下来的是第三个表dfs[2]。事实上该网页有多个表，如果抓取其他网站信息的时候需要打印出dfs，自己判断。

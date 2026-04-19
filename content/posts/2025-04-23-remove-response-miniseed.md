---
title: 去仪器响应练习
tags:
  - python
categories:
  - seismology
abbrlink: 6d0f71ef
date: 2025-04-23 15:14:23
---
用我的脚本下载了一堆的miniseed放在seed下，仪器响应文件放在resp文件夹下，利用obspy去除仪器响应，还保存为miniseed。
```
import os
from glob import glob
from obspy import read, read_inventory
# 设置路径
seed_folder = "seed"
resp_folder = "resp"
output_folder = "seed_corrected"
os.makedirs(output_folder, exist_ok=True)
seed_files = glob(os.path.join(seed_folder, "*.seed"))   # 遍历所有 seed 文件
for seed_file in seed_files:
    print(f"Processing {os.path.basename(seed_file)}")
    try:
        st = read(seed_file)   # 读取 MiniSEED 数据
        for tr in st:
            net = tr.stats.network
            sta = tr.stats.station
            loc = tr.stats.location
            cha = tr.stats.channel
            resp_file = os.path.join(resp_folder, f"RESP.{net}.{sta}.{loc}.{cha}") # 构造 RESP 文件路径
            if not os.path.exists(resp_file):
                print(f"RESP file not found: {resp_file}, skipping trace.")
                continue
            inventory = read_inventory(resp_file)   # 读取 RESP 文件作为 inventory
            # 去除仪器响应
            tr.remove_response(inventory=inventory, output="VEL", pre_filt=[0.001, 0.002, 0.3, 0.45 ], zero_mean=True, taper=True)
        output_file = os.path.join(output_folder, os.path.basename(seed_file)) # 输出文件名
        st.write(output_file, format="MSEED")
        print(f"Saved corrected data to {output_file}\n")
    except Exception as e:
        print(f"Error processing {seed_file}: {e}")
```

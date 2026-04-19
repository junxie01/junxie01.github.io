---
title: python脚本下载连续波形数据
tags:
  - python
categories:
  - work
abbrlink: b4ccc3e7
date: 2025-06-07 17:09:37
---
&emsp;&emsp;这是连续波形数据下载python脚本更新。
<!--less-->
```python
import os
import time
import socket
import numpy as np
from obspy import UTCDateTime, Stream
from obspy.clients.fdsn import Client
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import ConnectionError, Timeout

# 参数设置
client = Client("IRIS")
output_dir = "global_data"
os.makedirs(output_dir, exist_ok=True)
sta_file = "station.lst"
start_date = UTCDateTime("2013-01-01")
end_date = UTCDateTime("2024-01-01")  # 包括该天
thread_workers = 20
exception_log = "exceptions.txt"
timing_log = "download_time.txt"
max_retries = 5  # 最大重试次数
print(f"📁 当前工作目录: {os.getcwd()}")
print(f"📁 波形保存路径: {os.path.abspath(output_dir)}")

# 读取台站列表
sta_list = []
with open(sta_file, "r") as sf:
    for line in sf:
        if line.strip() and not line.strip().startswith("#"):
            parts = line.strip().split()
            if len(parts) >= 2:
                net, sta = parts[0], parts[1]
                sta_list.append((net, sta))

def download_station(net, sta, day):
    """
    下载单个台站某天波形数据，去仪器响应，返回Stream
    """
    start = UTCDateTime(day)
    end = start + 86400
    st = client.get_waveforms(net, sta, "*", "LH?", start, end, attach_response=True)

    st.remove_response(output="VEL", pre_filt=(0.008, 0.01, 0.3, 0.4),
                       taper=True, zero_mean=True, taper_fraction=0.05)
    return st
def download_day(day):
    """
    下载某天所有台站数据，返回合并Stream和日志信息
    """
    stream_day = Stream()
    daily_log = []
    log_lines = []

    with ThreadPoolExecutor(max_workers=thread_workers) as executor:
        futures = {executor.submit(download_station, net, sta, day): (net, sta) for net, sta in sta_list}

        for future in as_completed(futures):
            net, sta = futures[future]
            try:
                st = future.result()
                stream_day += st
                print(f"✅ {net}.{sta} 下载成功（{len(st)} traces）")
                daily_log.append((net, sta, 1))
            except Exception as e:
                print(f"❌ {net}.{sta} 下载失败: {e}")
                daily_log.append((net, sta, 0))
                log_lines.append(f"{day.date} {net}.{sta} ❌ {e}")

    return stream_day, daily_log, log_lines

def is_network_error(e):
    """
    判断异常是否为网络相关异常
    """
    network_error_types = (ConnectionError, Timeout, socket.timeout, socket.error)
    return isinstance(e, network_error_types) or "timed out" in str(e).lower() or "connection" in str(e).lower()

# 主循环
current_day = start_date
while current_day <= end_date:
    filename = f"{current_day.strftime('%Y%m%d')}.mseed"
    filepath = os.path.join(output_dir, filename)

    # 先判断文件是否存在且非空
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        print(f"\n📆 {current_day.date} 文件已存在且非空，跳过下载。")
        current_day += 86400
        continue

    print(f"\n📆 正在处理日期: {current_day.date}")

    attempt = 0
    success = False
    day_start_time = time.time()

    while attempt < max_retries and not success:
        attempt += 1
        print(f"🔄 尝试第 {attempt} 次下载 {current_day.date} ...")

        try:
            stream_day, daily_log, log_lines = download_day(current_day)

            if len(stream_day) == 0:
                print(f"⚠️ {current_day.date} 没有下载到数据，准备重试...")
                raise ValueError("下载数据为空")

            # 保存合并后的波形
            stream_day.write(filepath, format="MSEED")
            print(f"💾 {filename} 保存成功（共 {len(stream_day)} traces）")
            success = True

            # 写入异常日志
            if log_lines:
                with open(exception_log, "a") as elog:
                    elog.write("\n".join(log_lines) + "\n")

        except Exception as e:
            print(f"❌ 下载异常: {e}")

            # 判断是否为网络错误
            if is_network_error(e):
                print("🌐 网络异常，等待5秒后重试...")
                time.sleep(5)
            else:
                print("⚠️ 非网络异常，仍将重试...")
                time.sleep(3)

    # 下载耗时记录
    day_duration = time.time() - day_start_time
    with open(timing_log, "a") as tlog:
        tlog.write(f"{current_day.date}: {day_duration:.2f} seconds\n")

    if not success:
        print(f"❌ {current_day.date} 下载失败，超过最大重试次数。请检查网络或日志。")

    current_day += 86400
```
&emsp;&emsp;这个脚本实现的功能包括：
   * 下载台站列表station.lst的2013-01-01到2024-01-01，LH?数据。
   * 每天的数据存储为global_data/YYYYMMDD.mseed。
   * 去仪器响应，保留VEL，滤波频率为0.008, 0.01, 0.3, 0.4。
   * 记录每天数据下载的耗时，保存在“download_time.txt”中。
   * 判断是否是网络中断错误，如果是则做5次尝试重新下载，每次间隔5秒。
   * 判断当天数据是否已经被下载，如果没有或者大小是0则开始下载。
   * 将错误输出到exceptions.txt中。
   * 每天数据下载时，启用20个进程进行下载。

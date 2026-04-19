---
title: 统计数据下载情况
tags:
  - python
categories:
  - work
abbrlink: dc8bc93b
date: 2025-06-07 19:48:45
---
&emsp;&emsp;数据下载好后怎么统计数据连续性？
<!--less-->
&emsp;&emsp;python脚本如下。
```python
import os
from obspy import read
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.dates as mdates
from collections import defaultdict
from matplotlib.transforms import blended_transform_factory

# ===== 配置 =====
data_dir = "daily_waveforms"  # 存放YYYYMMDD.mseed文件目录
station_file = "station.list"  # 台站列表，格式：NET STA（两列）
components = ["LHZ", "LHN", "LHE"]
start_year = 2020
end_year = 2020

# ===== 读取台站列表 =====
stations = []
with open(station_file, "r") as f:
    for line in f:
        if line.strip():
            net, sta = line.strip().split()[:2]
            stations.append((net, sta))

station_set = set(f"{net}.{sta}" for net, sta in stations)

# ===== 初始化 =====
station_dates = {comp: defaultdict(set) for comp in components}  # comp -> {net.sta -> set(date)}
station_file_sizes = defaultdict(int)  # 台站对应所有文件大小
total_files = 0
total_file_size = 0

# ===== 遍历所有mseed文件 =====
all_files = sorted(f for f in os.listdir(data_dir) if f.endswith(".mseed"))
for filename in all_files:
    filepath = os.path.join(data_dir, filename)

    size = os.path.getsize(filepath)
    total_files += 1
    total_file_size += size

    try:
        st = read(filepath)
    except Exception as e:
        print(f"读取文件失败 {filename}: {e}")
        continue

    # 解析文件日期 YYYYMMDD
    try:
        file_date = dt.strptime(filename[:8], "%Y%m%d").date()
    except Exception as e:
        print(f"无法解析日期 {filename}: {e}")
        continue

    for tr in st:
        net = tr.stats.network
        sta = tr.stats.station
        comp = tr.stats.channel[-3:]

        key = f"{net}.{sta}"
        if key not in station_set:
            continue
        if comp not in components:
            continue

        station_dates[comp][key].add(file_date)
        station_file_sizes[key] += size

print(f"共计读取文件数: {total_files}")
print(f"所有文件总大小: {total_file_size / (1024**2):.2f} MB")

# ===== 删除无有效数据台站 =====
for comp in components:
    keys_to_remove = [k for k, dates in station_dates[comp].items() if len(dates) == 0]
    for k in keys_to_remove:
        del station_dates[comp][k]

# ===== 输出有效天数统计文本 =====
for comp in components:
    with open(f"station_day_count_{comp}.txt", "w") as f:
        for key in sorted(station_dates[comp].keys()):
            f.write(f"{key} {len(station_dates[comp][key])}\n")

# ===== 台网颜色映射 =====
all_nets = sorted(set(net for net, sta in stations))
net_color_map = {net: cm.get_cmap("tab20")(i / max(len(all_nets)-1,1)) for i, net in enumerate(all_nets)}

# ===== 绘图函数 =====
def plot_component_availability(comp, station_dates_comp):
    valid_stations = sorted(station_dates_comp.keys(), key=lambda x: (x.split(".")[0], x.split(".")[1]))
    fig, ax = plt.subplots(figsize=(14, max(6, 0.3 * len(valid_stations))))

    def to_datetime(d):
        return dt(d.year, d.month, d.day)

    for idx, key in enumerate(valid_stations):
        net = key.split(".")[0]
        dates = sorted(station_dates_comp[key])
        x_vals = [to_datetime(d) for d in dates]
        ax.plot(x_vals, [idx]*len(dates), ".", color=net_color_map[net], markersize=2)

    ax.set_xlabel("时间")
    ax.set_ylabel("台站")
    ax.set_yticks(range(len(valid_stations)))
    ax.set_yticklabels(valid_stations, fontsize=5)

    ax.grid(True, linestyle=":", alpha=0.5)

    x_start = dt(start_year, 1, 1)
    x_end = dt(end_year, 12, 31)
    ax.set_xlim(x_start, x_end)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # 右侧外部标注台网名
    trans = blended_transform_factory(ax.transAxes, ax.transData)
    net_indices = defaultdict(list)
    for idx, key in enumerate(valid_stations):
        net = key.split(".")[0]
        net_indices[net].append(idx)

    for net, indices in net_indices.items():
        mid_idx = indices[len(indices)//2]
        color = net_color_map[net]
        ax.text(1.02, mid_idx, net, color=color, fontsize=8, fontweight='bold',
                verticalalignment='center', horizontalalignment='left',
                transform=trans)

    plt.savefig(f"{comp}_availability_2013_2022.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已保存图像: {comp}_availability_2013_2022.png")

# ===== 画三分量图 =====
for comp in components:
    plot_component_availability(comp, station_dates[comp])

# ===== 台网统计 =====
network_stats = defaultdict(lambda: {"total": 0, "valid": 0, "day_counts": []})

for net, sta in stations:
    network_stats[net]["total"] += 1

all_valid_keys = set()
for comp in components:
    all_valid_keys.update(station_dates[comp].keys())

for key in all_valid_keys:
    net = key.split(".")[0]
    days_list = [len(station_dates[comp].get(key, [])) for comp in components]
    valid_days = max(days_list)
    network_stats[net]["valid"] += 1
    network_stats[net]["day_counts"].append(valid_days)

print("\n台网统计汇总：")
print(f"{'Net':<6} {'Total':>6} {'Valid':>6} {'AvgDays':>10}")
print("-" * 32)
with open("network_summary_all_components.txt", "w") as f:
    f.write(f"{'Net':<6} {'Total':>6} {'Valid':>6} {'AvgDays':>10}\n")
    for net in sorted(network_stats.keys()):
        total = network_stats[net]["total"]
        valid = network_stats[net]["valid"]
        avg_days = np.mean(network_stats[net]["day_counts"]) if network_stats[net]["day_counts"] else 0
        line = f"{net:<6} {total:>6} {valid:>6} {avg_days:>10.1f}"
        print(line)
        f.write(line + "\n")

# ===== 总结 =====
print(f"\n文件总数: {total_files}")
print(f"文件总大小: {total_file_size/(1024**2):.2f} MB ({total_file_size/(1024**3):.2f} GB)")
```
&emsp;&emsp;这个脚本实现的功能包括：
   * 统计开始时间start_year到结束时间end_year的数据下载情况
   * 对LHZ、LHN和LHE分别进行统计。
   * 对统计结果进行可视化输出。
   * 横轴是时间，纵轴是台站名。不同台网用不同颜色标出。在图右侧标出台网名。
   * 输出文件network_summary_all_components.txt，给出台网包含台站数目，有效台站数目和各自平均天数。
   * 输出文件station_day_count_{comp}.txt，给出台站名和有效天数。
   * 输出文件总数，文件总大小。

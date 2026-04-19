---
title: PYTHON脚本练习（二）
tags:
  - python
categories:
  - python
abbrlink: 689a3f45
date: 2025-06-30 21:27:28
---
&emsp;&emsp;以下是python脚本练习2，功能为读取选定时间段内的hdf5文件，文件名形如20130512_cross_spec.hdf5。该文件总共有24段，每一段是一个小时某台阵平均互相关谱。然后画出这个互相关谱，保存为png格式图片。
<!--less-->
```python
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter


def parse_filename_to_start_time(filename):
    """从文件名推断数据起始时间"""
    date_str = filename.split('_')[0]  # 提取"20130512"
    return datetime.strptime(date_str, "%Y%m%d")  # 转为 datetime


def load_cross_spec_from_files(hdf5_dir, start_date, end_date):
    """读取目录下所有落在给定时间范围的互相关谱"""
    files = sorted([f for f in os.listdir(hdf5_dir) if f.endswith("_cross_spec.hdf5")])
    #files = sorted([f for f in os.listdir(hdf5_dir) if f.endswith("_power_spec.hdf5")])
    time_list = []
    spec_list = []
    for file in files:
        try:
            base_time = parse_filename_to_start_time(file)
        except Exception as e:
            print(f"跳过无法解析时间的文件：{file}")
            continue

        if not (start_date <= base_time <= end_date):
            continue

        file_path = os.path.join(hdf5_dir, file)
        with h5py.File(file_path, 'r') as f:
            for i in range(1,24):
                ds_name = f'window_{i}'
                if ds_name in f:
                    data = f[ds_name][:]
                    current_time = base_time + timedelta(hours=i)
                    time_list.append(current_time)
                    spec_list.append(data)
    return time_list, spec_list


def plot_spectrogram(time_list, spec_list, freqs=None, title="Cross Spectrogram", save_path=None):
    """绘制时间-频率图像"""
    if not time_list or not spec_list:
        print("没有数据可供绘图。")
        return

    spec_array = np.array(spec_list).T  # shape: freq x time
    #spec_array = spec_array - np.mean(spec_array, axis=1, keepdims=True)
    n_freq = spec_array.shape[0]

    if freqs is None:
        freqs = np.linspace(0.005, 0.1, n_freq)

    fig, ax = plt.subplots(figsize=(14, 6))
    time_nums = mdates.date2num(time_list)

    cax = ax.pcolormesh(time_nums, freqs, spec_array, shading='auto', cmap='inferno')
    #cax = ax.pcolormesh(time_nums, freqs, spec_array, shading='auto' )
    fig.colorbar(cax, label='Cross Spectral Amplitude')
    ax.set_title(title)
    ax.set_yscale('log')  # 设置纵轴为对数刻度
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Frequency (Hz)")
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.xticks(rotation=30)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"图像已保存到：{save_path}")

    plt.show()

# 设置参数
hdf5_dir = "output_1_0"  # HDF5 文件夹路径
start_date = datetime(2006, 5, 1)
end_date = datetime(2006, 5,31)
# 加载数据
time_list, spec_list = load_cross_spec_from_files(hdf5_dir, start_date, end_date)
# 绘图并保存为 PNG（可选）
plot_spectrogram(time_list, spec_list,
                 title=f"Cross Spectral Density ({start_date.date()} ~ {end_date.date()})",
                 save_path="cross_spectrogram_2006_1_0.png")
```

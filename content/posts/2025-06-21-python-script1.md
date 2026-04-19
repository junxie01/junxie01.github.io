---
title: PYTHON脚本练习（一）
tags:
  - python
categories:
  - python
abbrlink: 588cd39d
date: 2025-06-21 14:29:56
---
&emsp;&emsp;以下是python脚本练习1，功能包括：
  * 遍历目录events_20250619下所有子目录中以bhz.SAC_rm结尾的SAC文件；
  * 对这些数据进行窄带滤波，宽度为中心频率（周期分之一）的$\pm$5mHz，滤波器为4个极点0相位的Butterworth，滤波周期为arange(25,145,10)；
  * 计算窄带滤波后的每个周期的信噪比。信噪比定义为信号窗口内，波形包络的最大值比上噪声窗口的均方根。信号窗口定义为2.5-5km/s的到时。噪声窗定义为信号末端之后1000秒开始的1000秒长度的窗口。计算的信噪比写入到user0；
  * 将处理后的数据写到新的文件夹bp_sac中，文件名命名为z.year.jday.00.STA.bhz.period，仅保留信噪比大于3的数据。
  * 采用并行处理(8个cpu)。
  * 统计每个周期信噪比大于3的波形数据。
  * 统计每个周期信噪比大于3的波形的平均信噪比。
  * 将统计结构写入csv，并画出统计结果。
<!--less-->
```
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy import read
from obspy.signal.filter import envelope
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# 参数设置 
input_root = "events_20250619"
output_root = "bp_sac"
center_periods = np.arange(25, 150, 10)
bandwidth = 0.010
vmin, vmax = 2.5, 5.0
noise_offset, noise_len = 1000, 1000
snr_threshold = 3.0
max_workers = 8  # 根据 CPU 核心数调整

# 存储每个周期的 SNR 值
period_snr_map = defaultdict(list)

def process_file(filepath, root):
    results = []
    try:
        st = read(filepath)
        tr = st[0]
        sac = tr.stats.sac
    except Exception as e:
        print(f"跳过 {filepath}: {e}")
        return results

    if not hasattr(sac, "o") or not hasattr(sac, "dist"):
        return results

    dist = sac.dist
    starttime = tr.stats.starttime
    win_start = starttime + dist / vmax
    win_end = starttime + dist / vmin
    t = tr.times()
    abs_time = np.array([starttime + float(tt) for tt in t])

    for period in center_periods:
        fc = 1.0 / period
        fmin, fmax = fc - bandwidth / 2, fc + bandwidth / 2
        if fmin <= 0:
            continue
        tr_filt = tr.copy()
        tr_filt.detrend("demean")
        tr_filt.taper(0.05)
        tr_filt.filter("bandpass", freqmin=fmin, freqmax=fmax, corners=4, zerophase=True)
        env = envelope(tr_filt.data)
        idx_sig = np.where((abs_time >= win_start) & (abs_time <= win_end))[0]
        if len(idx_sig) == 0:
            continue
        signal_max = np.max(env[idx_sig])
        noise_start = win_end + noise_offset
        noise_end = noise_start + noise_len
        idx_noise = np.where((abs_time >= noise_start) & (abs_time <= noise_end))[0]
        if len(idx_noise) == 0:
            continue
        noise_rms = np.sqrt(np.mean(env[idx_noise] ** 2))
        snr = signal_max / noise_rms if noise_rms > 0 else 0

        if snr >= snr_threshold:
            tr_filt.stats.sac.user0 = snr
            year = tr.stats.starttime.year
            jday = tr.stats.starttime.julday
            station = tr.stats.station.lower()
            channel = tr.stats.channel.lower()
            outname = f"z.{year}.{jday:03d}.00.{station}.{channel}.{period:03d}"

            rel_dir = os.path.relpath(root, input_root)
            out_dir = os.path.join(output_root, rel_dir)
            os.makedirs(out_dir, exist_ok=True)
            outpath = os.path.join(out_dir, outname)
            tr_filt.write(outpath, format="SAC")

            results.append((period, snr))
            print(f"✔ 保存: {outname}, SNR={snr:.2f}")

    return results
# ===== 收集所有文件路径 =====
all_files = []
for root, dirs, files in os.walk(input_root):
    for file in files:
        if file.endswith("bhz.SAC_rm"):
            all_files.append((os.path.join(root, file), root))

print(f"📁 待处理文件数: {len(all_files)}")

# ===== 并行处理 =====
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_file = {executor.submit(process_file, fpath, root): (fpath, root) for fpath, root in all_files}
    for future in as_completed(future_to_file):
        try:
            result = future.result()
            for period, snr in result:
                period_snr_map[period].append(snr)
        except Exception as e:
            fpath, _ = future_to_file[future]
            print(f"❌ 文件出错 {fpath}: {e}")

# ===== 统计与可视化 =====
periods = sorted(period_snr_map.keys())
counts = [len(period_snr_map[p]) for p in periods]
means = [np.mean(period_snr_map[p]) if len(period_snr_map[p]) > 0 else 0 for p in periods]

df = pd.DataFrame({
    "Period(s)": periods,
    "Count(SNR>3)": counts,
    "Mean_SNR(SNR>3)": means
})
df.to_csv("snr_stats.csv", index=False)

# === 可视化 ===
plt.figure(figsize=(10, 6))
plt.bar(periods, counts, width=4, color='skyblue', edgecolor='black')
plt.xlabel("Period (s)")
plt.ylabel("Count of SNR > 3")
plt.title("Number of Traces with SNR > 3 per Period")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("snr_count_bar.png", dpi=150)

plt.figure(figsize=(10, 6))
plt.plot(periods, means, marker='o', linestyle='-', color='orange')
plt.xlabel("Period (s)")
plt.ylabel("Mean SNR (SNR > 3)")
plt.title("Mean SNR of Traces with SNR > 3 per Period")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("snr_mean_line.png", dpi=150)

print("🎉 并行处理完成，统计结果写入 snr_stats.csv")
```

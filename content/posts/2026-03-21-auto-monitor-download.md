---
title: 自动监控地震数据下载脚本
categories:
  - work
tags:
  - python
abbrlink: f0f5a037
date: 2026-03-21 17:40:39
---
&emsp;&emsp;又是一个python下载地震数据的脚本，不过这次更好玩一些。设置一下就可以定期到USGS官网看看有没有大于某个震级的地震，然后到IRIS下载。
<!--less-->
&emsp;&emsp;老早就想这么搞了，在AI的帮助下终于搞定了啊。我把readme放下面了。
# Earthquake Auto-Monitor & Downloader (地震自动监测与补全下载工具)

这是一个基于 Python 和 ObsPy 的自动化地震数据处理工具。它能够定期监测 USGS 的地震发布信息，自动下载符合条件的地震波形数据，进行仪器响应去除、格式转换、头段读写以及波形可视化。

## ✨ 主要功能

1.  **自动化监测**：
    *   定期检索 USGS 目录中过去 12 小时内发生的 $M \ge 6.0$ 地震事件。
2.  **智能时长管理**：
    *   目标下载时长为 **2 小时**。
    *   **动态下载**：如果地震刚刚发生，程序会先下载发震至今的所有可用数据。
    *   **自动补全**：程序会检查 `download_status.txt`。如果已下载时长不足 2 小时，且现在有更多新数据可用，程序会自动删除旧数据并重新下载补全至最新时刻（最高 2 小时）。
3.  **标准化存储与命名**：
    *   **文件夹命名**：`YYYYMMDDHHMMSSM[震级]` (例如：`20231101123045M6.5`)。
    *   **SAC 文件命名**：`台网_台站_通道.SAC` (例如：`IU_ANMO_BHZ.SAC`)。
    *   **状态文件**：每个目录包含 `download_status.txt`，记录下载台站数、时长及下载时间。
4.  **科学级预处理**：
    *   去趋势 (Demean/Linear)、分段平滑 (Taper)。
    *   **去仪器响应**：将 Counts 转换为**速度分量 (m/s)**。
    *   **SAC 头段写入**：在 SAC 文件中自动写入：
        *   震源信息：`evla`, `evlo`, `evdp`, `mag`, `o` (发震时刻)。
        *   台站信息：`stla`, `stlo`, `stel`。
        *   距离信息：`garc` (大圆路径度数)。
5.  **多频带可视化**：
    *   自动生成两个频带的 Record Section 记录图：
        *   **长周期**：0.01 - 0.1 Hz
        *   **短周期**：0.1 - 2.0 Hz
    *   每张图包含左（Z）、中（N/1）、右（E/2）三个分量，按震中距排列。

## 🛠️ 安装要求

### 1. Python 环境
推荐使用 Python 3.8 或更高版本。

### 2. 依赖库
安装 ObsPy 及其绘图依赖：

```bash
pip install obspy matplotlib numpy
```

## 🚀 快速开始

### 1. 运行程序
直接运行脚本即可开始检索：

```bash
python auto_seismo_monitor.py
```

### 2. 设置定时任务 (推荐)
为了实现每 12 小时自动运行一次，建议设置定时任务。

#### **macOS / Linux (crontab)**
1. 输入 `crontab -e`。
2. 添加以下内容（注意修改路径）：

```cron
# 每 12 小时执行一次（0点和12点）
0 */12 * * * /usr/bin/python3 /Users/junxie/Work/auto_download/auto_seismo_monitor.py >> /Users/junxie/Work/auto_download/log.txt 2>&1
```

#### **Windows (任务计划程序)**
1. 创建基本任务，设置触发器为“每天”。
2. 在高级设置中选择“重复任务间隔”为“12 小时”。
3. 启动程序选择 `python.exe`，参数为脚本的完整路径。

## 📂 项目结构

```text
auto_download/
├── auto_seismo_monitor.py    # 主程序脚本
├── README.md                 # 说明文档
├── earthquake_data/          # 数据输出根目录
│   └── 20231101123045M6.5/   # 单个地震事件目录
│       ├── SAC_files/        # SAC 格式波形文件
│       ├── download_status.txt # 下载状态及时长说明
│       ├── plot_0.01_0.1Hz.png # 长周期波形图
│       └── plot_0.1_2Hz.png    # 短周期波形图
└── log.txt                   # 运行日志（设置crontab后生成）
```

## ⚙️ 配置说明

您可以在 `auto_seismo_monitor.py` 开头的“配置参数”部分调整：
*   `MIN_MAGNITUDE`: 触发下载的最小震级。
*   `TARGET_DURATION`: 目标下载时长（秒）。
*   `NETWORKS`: 下载的全球台网范围（默认为 IU, II, CU, IC, GE 等骨干台网）。
*   `OUTPUT_ROOT`: 数据保存的绝对路径。

## ⚠️ 注意事项
*   下载全球地震数据需要稳定的国际网络环境（访问 IRIS FDSN 服务）。
*   全球 BH? 数据量较大，请确保运行环境有充足的内存和磁盘空间。

有兴趣可以下载[Python脚本](/scripts/auto_seismo_monitor.py)试试，修改一下目录就可以了。


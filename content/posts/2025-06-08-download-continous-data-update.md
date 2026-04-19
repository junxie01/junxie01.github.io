---
title: python脚本下载连续波形数据更新
tags:
  - python
categories:
  - python
abbrlink: 5f341ab1
date: 2025-06-08 20:42:13
---
&emsp;&emsp;python脚本下载连续波形数据更新。
<!--less-->
```python
import os
import numpy as np
from obspy import UTCDateTime, Stream, Trace
from obspy.io.sac import SACTrace
from obspy.clients.fdsn import Client
from obspy.signal.rotate import rotate_ne_rt
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from collections import defaultdict

# 参数设置
client = Client("IRIS")
output_dir = "daily_waveforms"
os.makedirs(output_dir, exist_ok=True)
sta_file = "station.list"
start_date = UTCDateTime("2023-09-16")
end_date = UTCDateTime("2023-09-27")  # 包括该天
thread_workers = 6
exception_log = "exceptions.txt"
sampling_rate = 1.0  # LH通道的采样率 (1 Hz)
expected_npts = 86400  # 86400秒 * 1Hz采样率

# 打印工作目录与输出目录
print(f"📁📁📁📁 当前工作目录: {os.getcwd()}")
print(f"📁📁📁📁 保存路径: {os.path.abspath(output_dir)}")

# 读取台站列表
sta_list = []
with open(sta_file, "r") as sf:
    for line in sf:
        if line.strip() and not line.strip().startswith("#"):
            parts = line.strip().split()
            if len(parts) >= 2:
                net, sta = parts[0], parts[1]
                sta_list.append((net, sta))

# 记录异常到文件
def log_exception(msg):
    with open(exception_log, "a") as f:
        f.write(f"{UTCDateTime.now().isoformat()} - {msg}\n")

# 保存为SAC文件（每个通道一个文件）
def save_channel_sac(tr, day_dir, net, sta, station_coords):
    try:
        # 确保目录存在
        os.makedirs(day_dir, exist_ok=True)
        
        # 文件名格式: NET_STA_CHAN.SAC
        chan = tr.stats.channel
        filename = f"{net}_{sta}_{chan}.SAC"
        filepath = os.path.join(day_dir, filename)
        
        # 创建SACTrace对象
        sac = SACTrace.from_obspy_trace(tr)
        
        # 设置台站信息
        sac.kstnm = sta
        sac.knetwk = net
        
        # 设置坐标信息
        if station_coords is not None:
            sac.stla = station_coords["latitude"]
            sac.stlo = station_coords["longitude"]
            sac.stel = station_coords["elevation"]
            sac.stdp = station_coords.get("local_depth", 0.0)
            print(f"    ✅ 添加坐标: {sac.stla:.4f}, {sac.stlo:.4f}")
        else:
            sac.stla = 0.0
            sac.stlo = 0.0
            sac.stel = 0.0
            sac.stdp = 0.0
            print(f"    ⚠⚠⚠️ 无坐标信息")
        
        # 保存文件
        sac.write(filepath)
        
        print(f"  保存: {filename}")
        return filepath
    except Exception as e:
        log_exception(f"保存SAC文件失败 {net}.{sta}.{chan}: {str(e)}")
        traceback.print_exc()
        return None

# 数据补零处理
def fill_gaps(tr, start_time):
    """
    确保数据有完整的86400个点，缺失部分补零
    """
    try:
        # 创建新的头信息
        new_header = tr.stats.copy()
        new_header.starttime = start_time  # 确保从当天00:00:00开始
        new_header.npts = expected_npts
        new_header.sampling_rate = sampling_rate
        
        # 创建全零数据数组
        new_data = np.zeros(expected_npts, dtype=tr.data.dtype)
        
        # 计算数据偏移量（当前数据在当天中的起始位置）
        start_diff = int((tr.stats.starttime - start_time))
        
        # 确保偏移量在合理范围内
        if 0 <= start_diff < expected_npts:
            end_index = min(start_diff + tr.stats.npts, expected_npts)
            valid_length = end_index - start_diff
            
            # 将实际数据复制到全零数组的相应位置
            if valid_length > 0:
                new_data[start_diff:end_index] = tr.data[:valid_length]
        
        # 创建新的Trace
        return Trace(data=new_data, header=new_header)
    except Exception as e:
        log_exception(f"数据补零失败: {str(e)}")
        return tr

# 旋转LH1/LH2分量到LHE/LHN
def rotate_to_EN(tr1, tr2):
    """将两个水平分量(LH1/LH2)旋转到地理坐标系(LHE/LHN)"""
    try:
        # 假设LH1是北分量，LH2是东分量
        north = tr1.data
        east = tr2.data
        
        # 旋转分量
        n, e = rotate_ne_rt(north, east, 0)
        
        # 创建新的Trace对象
        trN = Trace(data=n)
        trN.stats = tr1.stats.copy()
        trN.stats.channel = "LHN"
        
        trE = Trace(data=e)
        trE.stats = tr2.stats.copy()
        trE.stats.channel = "LHE"
        
        return trN, trE
    except Exception as e:
        log_exception(f"旋转分量失败: {e}")
        return tr1, tr2

# 处理水平分量
def process_horizontal_components(st):
    """
    处理水平分量：
    1. 如果只有LH1和LH2，旋转为LHE和LHN，并删除原始的极LH1/LH2
    2. 如果存在LHN和LHE，优先使用它们，并删除任何LH1/LH2分量
    """
    try:
        # 按通道类型分组
        comp_groups = defaultdict(list)
        for tr in st:
            comp_groups[tr.stats.channel].append(tr)
        
        # 处理水平分量
        horizontal_stream = Stream()
        
        # 优先选择LHN和LHE分量
        en_comps = ["LHE", "LHN"]
        has_EN = any(comp in comp_groups for comp in en_comps)
        
        if has_EN:
            # 使用已有的LHN/LHE分量（只取第一个）
            for comp in en_comps:
                if comp in comp_groups:
                    horizontal_stream.append(comp_groups[comp][0])
            print("  使用现有的LHN/LHE分量")
            
            # 删除任何存在的LH1/LH2分量
            if "LH1" in comp_groups or "LH2" in comp_groups:
                print("  删除原始的LH1/LH2分量")
        else:
            # 检查是否有LH1和LH2
            rt_comps = ["LH1", "LH2"]
            if all(comp in comp_groups for comp in rt_comps):
                # 获取LH1和LH2分量（只取第一个）
                lh1 = comp_groups["LH1"][0]
                lh2 = comp_groups["LH2"][0]
                
                # 旋转到EN分量
                trN, trE = rotate_to_EN(lh1, lh2)
                horizontal_stream.append(trN)
                horizontal_stream.append(trE)
                print("  旋转LH1/LH2为LHN/LHE")
                
                # 删除原始的LH1/LH2分量
                print("  删除原始的LH1/LH2分量")
        
        return horizontal_stream
    except Exception as e:
        log_exception(f"处理水平分量失败: {e}")
        return Stream()

# 下载并处理单个台站某天的数据
def download_station(net, sta, day):
    station_coords = None  # 存储台站坐标
    try:
        start = UTCDateTime(day)
        end = start + 86400
        day_str = start.strftime("%Y%m%d")
        
        # 获取台站元数据
        print(f"  获取 {net}.{sta} 元数据...")
        try:
            inv = client.get_stations(
                network=net, 
                station=sta, 
                starttime=start, 
                endtime=end, 
                level="channel"
            )
            
            # 尝试获取台站坐标（使用LHZ通道）
            try:
                station_coords = inv.get_coordinates(f"{net}.{sta}.00.LHZ", start)
                print(f"    ✅ 获取坐标: {station_coords['latitude']:.4f}, {station_coords['longitude']:.4f}")
            except:
                # 如果LHZ失败，尝试其他LH通道
                for chan in ["LHN", "LHE", "LH1", "LH2"]:
                    try:
                        station_coords = inv.get_coordinates(f"{net}.{sta}.00.{chan}", start)
                        print(f"    ✅ 获取坐标: {station_coords['latitude']:.4f}, {station_coords['longitude']:.4f}")
                        break
                    except:
                        continue
                if station_coords is None:
                    print("    ⚠⚠⚠️ 无法获取坐标")
        except Exception as e:
            print(f"  ⚠⚠⚠️ 元数据获取失败: {str(e)}")
        
        # 下载波形数据
        print(f"  下载 {net}.{sta} 波形数据...")
        st = client.get_waveforms(net, sta, "*", "LH?", start, end, attach_response=True)
        
        # 如果没数据，直接返回
        if len(st) == 0:
            return (net, sta, False, "无数据")
        
        # 检查是否有LHZ分量（只取第一个）
        vertical_st = st.select(channel="LHZ")
        if len(vertical_st) == 0:
            print(f"  ⚠⚠⚠️ 跳过 {net}.{sta} - 无LHZ分量")
            return (net, sta, False, "无LHZ分量")
        else:
            # 只保留第一个LHZ分量
            vertical_tr = vertical_st[0]
        
        # 去除仪器响应
        print("  去除仪器响应...")
        st.remove_response(output="VEL", pre_filt=(0.008, 0.01, 0.3, 0.4),
                           taper=True, zero_mean=True, taper_fraction=0.05)
        
        # 处理水平分量
        print("  处理水平分量...")
        horizontal_st = process_horizontal_components(st)
        
        # 合并垂直和水平分量
        processed_st = Stream([vertical_tr]) + horizontal_st
        
        # 确保只有三个分量：LHZ, LHN, LHE
        final_st = Stream()
        channels = set()
        for tr in processed_st:
            # 只添加LHZ、LHN和LHE分量
            if tr.stats.channel in ["LHZ", "LHN", "LHE"]:
                if tr.stats.channel not in channels:
                    final_st.append(tr)
                    channels.add(tr.stats.channel)
                else:
                    print(f"  ⚠⚠⚠️ 跳过重复通道: {tr.stats.channel}")
        
        # 数据补零处理
        print("  数据补零处理...")
        filled_st = Stream()
        for tr in final_st:
            filled_tr = fill_gaps(tr, start)
            filled_st.append(filled_tr)
        
        # 创建日期目录
        day_dir = os.path.join(output_dir, day_str)
        
        # 保存每个通道的数据
        saved_files = []
        for tr in filled_st:
            filepath = save_channel_sac(tr, day_dir, net, sta, station_coords)
            if filepath:
                saved_files.append(filepath)
        
        return (net, sta, True, saved_files)
    except Exception as e:
        error_msg = f"{str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" (Status: {e.response.status_code})"
        return (net, sta, False, error_msg)

# 遍历日期，按天下载并保存
current_day = start_date
while current_day <= end_date:
    day_str = current_day.strftime("%Y%m%d")
    day_dir = os.path.join(output_dir, day_str)
    
    # 检查是否已下载
    if os.path.exists(day_dir) and os.path.isdir(day_dir):
        print(f"\n📆📆📆📆 日期 {current_day.date} 已存在，跳过处理")
        # 进入下一天
        current_day += 86400
        continue
    
    print(f"\n📆📆📆📆 正在处理日期: {current_day.date}")
    
    # 创建日期目录
    os.makedirs(day_dir, exist_ok=True)

    # 异常记录每天追加
    log_lines = []
    success_count = 0
    fail_count = 0

    # 启动多线程下载当天所有台站数据
    with ThreadPoolExecutor(max_workers=thread_workers) as executor:
        futures = {executor.submit(download_station, net, sta, current_day): (net, sta) for net, sta in sta_list}

        for future in as_completed(futures):
            net, sta = futures[future]
            try:
                net, sta, ok, result = future.result()
                if ok:
                    success_count += 1
                    file_count = len(result)
                    print(f"✅ {net}.{sta} 处理成功 - 保存了 {file_count} 个SAC文件")
                    for filepath in result:
                        print(f"   ↳↳ {os.path.basename(filepath)}")
                else:
                    fail_count += 1
                    print(f"❌❌❌❌ {net}.{sta} 处理失败: {result}")
                    log_lines.append(f"{current_day.date} {net}.{sta} ❌❌❌❌ {result}")
            except Exception as e:
                fail_count += 1
                error_msg = f"{str(e)}"
                print(f"❌❌❌❌ {net}.{sta} 异常: {error_msg}")
                log_lines.append(f"{current_day.date} {net}.{sta} ❌❌❌❌ {error_msg}")
                traceback.print_exc()

    print(f"\n📊📊 本日统计: {success_count} 个台站成功, {fail_count} 个台站失败")

    # 写入异常日志
    if log_lines:
        with open(exception_log, "a") as elog:
            elog.write("\n".join(log_lines) + "\n")

    # 进入下一天
    current_day += 86400

print("\n🎉🎉 所有日期处理完成!")
```
&emsp;&emsp;此脚本完成以下操作:
   * 多线程下载指定定时间段的LH分量数据。
   * 按天保存到同一个文件夹，检查当天的文件是否已经建立，如果已建立则跳过（防止重复下载）。
   * 检查是否有LHZ分量，如果没有则跳过此台。
   * 去除仪器响应，保存为速度记录，滤波到0.008-0.4Hz。
   * 仅保存第一个location（空，00，01）的LHZ，LHE，LHN。
   * 如果同时有LH1,LH2,LHE,LHN则删除LH1,LH2分量。
   * 如果仅有LH1,LH2,则旋转到LHE，LHN，删除LH1,LH2。
   * 如果不足86400则补零，对齐到当天的00:00:00。
   * 保存为SAC格式，文件名为NET_STA_COM.SAC。

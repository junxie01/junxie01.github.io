---
title: 下载地震数据练习
tags:
  - python
categories:
  - seismology
abbrlink: ca92bb2a
date: 2025-04-24 15:33:35
---
&emsp;&emsp;地震波形数据怎么下载？
<!--less-->
&emsp;&emsp;可以去[IRIS](http://iris.edu/)网站下啊。这里给出结合FetchEvent和obspy进行数据下载的例子，还比较简单哈。
&emsp;&emsp;FetchEvent从地址https://github.com/EarthScope/fetch-scripts下载。他是用perl脚本写的。运行例子如下：
```
./FetchEvent -s 2006-01-01 -e 2007-05-01 --radius 5:12:95:28 --mag 5:10 -o event.lst
```
&emsp;&emsp;表示下载发生时间为2006-01-01到2007-05-01，位于以(5,12)(lat,lon)为中心，半径28-95度，震级5-10级的地震信息，保存到event.lst中。
&emsp;&emsp;下载到的event.lst内容如下：
```
8037834 |2006/01/23 20:50:46.19Z |  6.9168| -77.7951|  24.0355|ISC|||MS,5.86,ISC|mb,6.16,ISC|Near west coast of Colombia
```
&emsp;&emsp;表示ID|时间|纬度|经度|深度|目录|||震级类型,震级,目录|震级类型,震级,目录|位置
&emsp;&emsp;可以看出地震信息来自ISC目录，其实到[ISC](https://www.isc.ac.uk/iscbulletin/search/catalogue/)直接检索也很方便。

&emsp;&emsp;接下来，下载XB台网所有台站接收到的地震理论P波到时前50秒到后150秒三分量数据。其中P波到时调用taup来计算。接下来去仪器响应，最后再截取P波前10秒到后60秒。保存为SAC格式，每个地震每个台站保存一个SAC，名称需包含地震时间震级及台站名。利用多线程ThreadPoolExecutor加速。脚本如下：
```
import os
from obspy import UTCDateTime, read_inventory
from obspy.clients.fdsn import Client
from obspy.taup import TauPyModel
from obspy.geodetics import locations2degrees
from concurrent.futures import ThreadPoolExecutor, as_completed

client = Client("IRIS")
model = TauPyModel("iasp91")

output_dir = "processed_sac"
os.makedirs(output_dir, exist_ok=True)

event_file = "event.lst"
exception_log = "exceptions.txt"
thread_workers = 4  # 可调线程数

with open(event_file, "r") as f:
    event_lines = [line.strip() for line in f if line.strip()]

with open(exception_log, "w") as elog:
    elog.write("")

def process_station(event_id, origin_time, magnitude, ev_lat, ev_lon, ev_dep, net, sta, sta_lat, sta_lon, sta_elev):
    try:
        # 使用 locations2degrees 计算震中距
        dist_deg = locations2degrees(ev_lat, ev_lon, sta_lat, sta_lon)
        print(dist_deg)
        arrivals = model.get_travel_times(source_depth_in_km=ev_dep,
                                          distance_in_degree=dist_deg,
                                          phase_list=["P"])
        if not arrivals:
            raise Exception("No P arrival")

        p_arrival = origin_time + arrivals[0].time
        start_dl = p_arrival - 50
        end_dl = p_arrival + 150

        # 下载三分量数据
        st = client.get_waveforms(network=net, station=sta, location="*", channel="BH?",
                                  starttime=start_dl, endtime=end_dl,
                                  attach_response=True)

        # 去响应
        st.remove_response(output="VEL", pre_filt=(0.01, 0.02, 8, 10), taper=True, zero_mean=True, taper_fraction=0.05)

        # 截取有效窗口
        st.trim(starttime=p_arrival - 10, endtime=p_arrival + 60)

        # 检查是否为三分量
        if not all(comp in [tr.stats.channel[-1] for tr in st] for comp in ["N", "E", "Z"]):
            raise Exception("Incomplete 3-component data")

        # 写入 SAC 文件并添加头段信息
        for tr in st:
            tr.stats.sac = tr.stats.get("sac", {})
            tr.stats.sac.stla = sta_lat
            tr.stats.sac.stlo = sta_lon
            tr.stats.sac.stel = sta_elev
            tr.stats.sac.evla = ev_lat
            tr.stats.sac.evlo = ev_lon
            tr.stats.sac.evdp = ev_dep
            tr.stats.sac.mag = float(magnitude) if magnitude != "NA" else 0.0

            time_tag = origin_time.strftime("%Y%m%dT%H%M%S")
            chan = tr.stats.channel
            filename = f"{time_tag}_M{magnitude}_{net}.{sta}.{chan}.sac"
            filepath = os.path.join(output_dir, filename)
            tr.write(filepath, format="SAC")
        return f"{net}.{sta} ✅"
    except Exception as e:
        with open(exception_log, "a") as elog:
            elog.write(f"{event_id} {net}.{sta} ❌ {str(e)}\n")
        return f"{net}.{sta} ❌ {str(e)}"

def process_event(line):
    results = []
    parts = line.split("|")
    if len(parts) < 10:
        return ["跳过格式错误行"]

    evid = parts[0].strip()
    time_str = parts[1].strip()
    ev_lat = float(parts[2].strip())
    ev_lon = float(parts[3].strip())
    ev_dep = float(parts[4].strip())
    mag_info = parts[8].strip()
    magnitude = mag_info.split(",")[1] if "," in mag_info else "NA"

    origin_time = UTCDateTime(time_str)
    print(f"\n🟡 Processing event {evid} M{magnitude} @ {origin_time} ({ev_lat}, {ev_lon}, {ev_dep}km)")

    try:
        inventory = client.get_stations(network="XB", starttime=origin_time,
                                        endtime=origin_time + 3600,
                                        level="station", channel="BH?")
        task_list = []
        with ThreadPoolExecutor(max_workers=thread_workers) as executor:
            for network in inventory:
                for station in network:
                    sta_lat = station.latitude
                    sta_lon = station.longitude
                    sta_elev = station.elevation
                    sta = station.code
                    net = network.code
                    task = executor.submit(process_station, evid, origin_time, magnitude,
                                           ev_lat, ev_lon, ev_dep, net, sta, sta_lat, sta_lon, sta_elev)
                    task_list.append(task)

            for task in as_completed(task_list):
                results.append(task.result())

    except Exception as e:
        with open(exception_log, "a") as elog:
            elog.write(f"{evid} XB ERROR: {str(e)}\n")
        results.append(f"⚠️ Failed to process event {evid}: {e}")
    return results

# 执行所有事件处理
for line in event_lines:
    results = process_event(line)
    for r in results:
        print(r)
```

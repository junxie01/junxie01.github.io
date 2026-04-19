---
title: 下载地震数据更新
tags:
  - python
categories:
  - seismology
abbrlink: a1dc7bf4
date: 2025-05-16 14:39:46
---
&emsp;&emsp;要是指定台站列表怎么下载地震数据呢？
<!--less-->
&emsp;&emsp;python脚本如下。
```
import os
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.taup import TauPyModel
from obspy.geodetics import locations2degrees
from concurrent.futures import ThreadPoolExecutor, as_completed

client = Client("IRIS")
model = TauPyModel("iasp91")

output_dir = "processed_sac"
os.makedirs(output_dir, exist_ok=True)

event_file = "event.lst"
sta_file = "sta.lst"
exception_log = "exceptions.txt"
thread_workers = 4

# 读取台站信息：net, sta, lat, lon, elev
with open(sta_file, "r") as sf:
    sta_lines = [line.strip() for line in sf if line.strip()]
sta_list = []
for line in sta_lines:
    parts = line.split("|")
    if len(parts) >= 5:
        net = parts[0].strip()
        sta = parts[1].strip()
        lat = float(parts[2])
        lon = float(parts[3])
        elev = float(parts[4])
        sta_list.append((net, sta, lat, lon, elev))

# 清空异常日志
with open(exception_log, "w") as elog:
    elog.write("")

def process_station(event_id, origin_time, magnitude, ev_lat, ev_lon, ev_dep,
                    net, sta, sta_lat, sta_lon, sta_elev):
    try:
        dist_deg = locations2degrees(ev_lat, ev_lon, sta_lat, sta_lon)
        arrivals = model.get_travel_times(source_depth_in_km=ev_dep,
                                          distance_in_degree=dist_deg,
                                          phase_list=["P"])
        if not arrivals:
            raise Exception("No P arrival")

        p_arrival = origin_time + arrivals[0].time
        start_dl = p_arrival - 50
        end_dl = p_arrival + 150

        st = client.get_waveforms(network=net, station=sta, location="*", channel="BH?",
                                  starttime=start_dl, endtime=end_dl,
                                  attach_response=True)

        st.remove_response(output="VEL", pre_filt=(0.01, 0.02, 8, 10),
                           taper=True, zero_mean=True, taper_fraction=0.05)

        st.trim(starttime=p_arrival - 10, endtime=p_arrival + 60)

        comps = [tr.stats.channel[-1] for tr in st]
        if not all(comp in comps for comp in ["N", "E", "Z"]):
            raise Exception("Incomplete 3-component data")

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
        task_list = []
        with ThreadPoolExecutor(max_workers=thread_workers) as executor:
            for net, sta, sta_lat, sta_lon, sta_elev in sta_list:
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

# 读取事件列表并执行
with open(event_file, "r") as f:
    event_lines = [line.strip() for line in f if line.strip()]

for line in event_lines:
    results = process_event(line)
    for r in results:
        print(r)
```
&emsp;&emsp;与之前的脚本:{% post_link 下载地震数据练习 %}不同的地方是多了文件sta.lst。其格式为：
TA|140A|32.6408|-93.573997|56.0|
台网|台站|纬度|经度|高程

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom FK / beamforming array analysis (no obspy.array_processing)
改进：使用速度 (km/s) 替代慢度，每天输出雷达图，并标注最大能量点
"""
import os
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime
from datetime import timedelta

# ---------------- User parameters ----------------
station_file = "station.lst"
data_dir = "data"                 # structure: data/YYYYMMDD/NET_STA_LH?.SAC
output_dir = "arr_figures"
os.makedirs(output_dir, exist_ok=True)

# frequency band of interest
fmin, fmax = 0.028, 0.032  # Hz

# window settings
win_len = 1800             # seconds
win_frac = 0.5             # 50% overlap
win_step = int(win_len * (1 - win_frac))

# FK grid
az_step = 5.0
az_grid = np.arange(0, 360, az_step)

# speed search (instead of slowness)
vmin, vmax, vstep = 1, 5.0, 0.05  # km/s
#s_grid = 1.0 / np.arange(vmax, vmin, -vstep)  # convert to slowness s/km
speed_grid = np.arange(vmin, vmax, vstep)  # convert to slowness s/km

#speed_grid = 1.0 / s_grid  # for plotting
s_grid = 1.0 / speed_grid  # for plotting

# day range
start_date = UTCDateTime("2013-01-01")
end_date   = UTCDateTime("2025-01-01")

# minimal number of stations
min_stations = 3

# ---------------- helper functions ----------------
def read_stations(station_file):
    stations = []
    with open(station_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 4:
                continue
            net, sta = parts[0].strip(), parts[1].strip()
            try:
                lat = float(parts[2]); lon = float(parts[3])
            except Exception:
                continue
            stations.append((net, sta, lat, lon))
    return stations

def geo_to_xy_km(lats, lons):
    lat0 = np.mean(lats)
    lon0 = np.mean(lons)
    deg2km_lat = 110.574
    deg2km_lon = 111.320 * math.cos(math.radians(lat0))
    xs = (np.array(lons) - lon0) * deg2km_lon
    ys = (np.array(lats) - lat0) * deg2km_lat
    return xs, ys, lat0, lon0

def window_slices(day_start, win_len, win_step):
    t0 = int(day_start.timestamp)
    t_end = int((day_start + 86400).timestamp)
    slices = []
    t = t0
    while t + win_len <= t_end:
        slices.append((t, t + win_len))
        t += win_step
    return slices

def next_pow2(n):
    return 1 << (n - 1).bit_length()

# ---------------- main pipeline ----------------
stations = read_stations(station_file)
if len(stations) == 0:
    raise SystemExit("No stations read from station.lst")

print(f"[INFO] Read {len(stations)} stations")

current = start_date
while current <= end_date:
    day_str = current.strftime("%Y%m%d")
    day_path = os.path.join(data_dir, day_str)
    print(f"\n[INFO] Processing {day_str} ...")
    if not os.path.isdir(day_path):
        print(f"[WARN] {day_path} not found. skip.")
        current += timedelta(days=1)
        continue

    # read one trace per station
    traces = {}
    lat_list = []; lon_list = []; net_sta_list = []
    for net, sta, lat, lon in stations:
        pattern = os.path.join(day_path, f"{net}_{sta}_LHZ.SAC")
        files = sorted(glob.glob(pattern))
        if not files: continue
        try:
            tr = read(files[0])[0]
            traces[(net,sta)] = tr
            lat_list.append(lat); lon_list.append(lon); net_sta_list.append((net,sta))
        except Exception as e:
            print(f"[WARN] read {files[0]} failed: {e}")
            continue

    nsta = len(traces)
    if nsta < min_stations:
        print(f"[WARN] Only {nsta} stations available, skip.")
        current += timedelta(days=1)
        continue

    # sampling rate
    sr_target = min([tr.stats.sampling_rate for tr in traces.values()])
    xs, ys, lat0, lon0 = geo_to_xy_km(lat_list, lon_list)

    # reorder traces
    traces_ordered = [traces[k] for k in net_sta_list]

    # window slices
    day_start = UTCDateTime(current.strftime("%Y-%m-%dT00:00:00"))
    slices = window_slices(day_start, win_len, win_step)
    print(f"[INFO] {len(slices)} windows")

    # accumulate daily power grid
    daily_power = np.zeros((len(az_grid), len(s_grid)))
    nwin_used = 0

    for (t0, t1) in slices:
        specs = []
        valid = True
        nfft = None
        for tr in traces_ordered:
            try:
                seg = tr.slice(UTCDateTime(t0), UTCDateTime(t1), nearest_sample=False)
            except:
                valid = False; break
            expected_npts = int(round((t1 - t0) * sr_target))
            data = seg.data.astype(np.float64)
            if len(data) < expected_npts:
                if len(data) == 0: valid = False; break
                data = np.pad(data, (0, expected_npts-len(data)))
            elif len(data) > expected_npts:
                data = data[:expected_npts]
            data -= np.mean(data)
            data *= np.hanning(len(data))
            if nfft is None:
                nfft = next_pow2(len(data))
            spec = np.fft.rfft(data, n=nfft)
            freqs = np.fft.rfftfreq(nfft, d=1.0/sr_target)
            specs.append(spec)
        if not valid or nfft is None: continue

        specs = np.array(specs)
        freq_mask = (freqs>=fmin)&(freqs<=fmax)
        if not np.any(freq_mask): continue
        freqs_sel = freqs[freq_mask]
        specs_sel = specs[:, freq_mask]

        xs_arr = np.array(xs); ys_arr = np.array(ys)
        spec_power = np.sum(np.abs(specs_sel)**2)
        if spec_power<=0: continue

        two_pi = 2*np.pi
        power_grid = np.zeros((len(az_grid), len(s_grid)))
        for ia, az_deg in enumerate(az_grid):
            az_rad = math.radians(az_deg)
            proj = xs_arr*np.sin(az_rad) + ys_arr*np.cos(az_rad)
            for is_idx, s in enumerate(s_grid):
                delays = proj*s
                steering = np.exp(-1j*two_pi*np.outer(delays,freqs_sel))
                beam_spectrum = np.sum(steering*specs_sel, axis=0)
                power = np.sum(np.abs(beam_spectrum)**2)
                power_grid[ia,is_idx] = power/spec_power
        daily_power += power_grid
        nwin_used += 1

    if nwin_used==0:
        print(f"[WARN] no valid windows {day_str}")
        current += timedelta(days=1)
        continue

    daily_power /= nwin_used
    print(f"[INFO] averaged over {nwin_used} windows")

    # ---------------- plot daily radar ----------------
    theta, r = np.meshgrid(np.deg2rad(az_grid), speed_grid)
    Z = daily_power.T  # shape (len(s_grid), len(az_grid))

    # locate max power
    max_idx = np.unravel_index(np.argmax(Z), Z.shape)
    max_az_deg = az_grid[max_idx[1]]
    max_speed = r[max_idx]  # km/s

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, polar=True)
    pcm = ax.pcolormesh(theta, r, Z, shading="auto", cmap="viridis")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rmax(vmax)
    #fig.colorbar(pcm, ax=ax, orientation="vertical", label="Normalized Power")
    ax.set_title(f"FK Radar {day_str}\nBand {fmin}-{fmax} Hz", fontsize=12)

    # mark max point
    ax.plot(np.deg2rad(max_az_deg), max_speed, 'ro', markersize=8, label=f"Max Power\nAz={max_az_deg:.1f}°, v={max_speed:.2f} km/s")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3,1.1), fontsize=8)

    out_png = os.path.join(output_dir, f"fk_radar_{day_str}.png")
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[INFO] saved {out_png}")
    current += timedelta(days=1)

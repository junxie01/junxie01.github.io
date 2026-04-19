---
title: obspy下载连续背景噪声数据
tags:
  - obspy
  - python
categories:
  - python
abbrlink: cb1143bd
date: 2025-04-21 21:17:55
---
利用obspy的MassDownloader下载连续的波形示例。
```python
import obspy
from obspy.clients.fdsn.mass_downloader import RectangularDomain, CircularDomain, \
    Restrictions, MassDownloader
# Rectangular domain containing parts of southern Germany.
#domain = RectangularDomain(minlatitude=-15, maxlatitude=18,
#                           minlongitude=10, maxlongitude=22)
domain = CircularDomain(
        latitude=0,
        longitude=0,
        minradius=0.0,
        maxradius=12.0
        )
restrictions = Restrictions(
    # Get data for a whole year.
    starttime=obspy.UTCDateTime(2005, 1, 15),
    endtime=obspy.UTCDateTime(2007, 10, 15),
    # Chunk it to have one file per day.
    chunklength_in_sec=86400,
    # Considering the enormous amount of data associated with continuous
    # requests, you might want to limit the data based on SEED identifiers.
    # If the location code is specified, the location priority list is not
    # used; the same is true for the channel argument and priority list.
    network="??", station="????", location="*", channel="LHZ",
    # The typical use case for such a data set are noise correlations where
    # gaps are dealt with at a later stage.
    reject_channels_with_gaps=False,
    # Same is true with the minimum length. All data might be useful.
    minimum_length=0.0,
    # Guard against the same station having different names.
    minimum_interstation_distance_in_m=100.0)
# Restrict the number of providers if you know which serve the desired
# data. If in doubt just don't specify - then all providers will be
# queried.
#mdl = MassDownloader(providers=["IRIS","USGS","GFZ"])
mdl = MassDownloader()
mdl.download(domain, restrictions, mseed_storage="waveforms",
             stationxml_storage="stations")
```

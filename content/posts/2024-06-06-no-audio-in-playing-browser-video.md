---
title: Fedora下浏览器播放视频卡住没有声音
categories:
  - Linux
tags:
  - linux
abbrlink: 4a2f0c3d
date: 2024-06-06 12:29:49
---
之前整了nodesk之后就出现了视频播放的问题。用mplayer播放视频时，卡住。用浏览器播放视频的时候卡住，关掉音频之后视频正常播放了。但是没有声音。
然后
```
systemctl --user stop wireplumber
```
关掉了wireplumber以后mplayer和浏览器上都能正常播放了。但每次重启都得运行一次。多麻烦呀。
然后
```
sudo dnf install --allowerasing pipewire-pulseaudio
```
就可以了。

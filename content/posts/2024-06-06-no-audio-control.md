---
title: Fedora下没有音量控制了
categories:
  - Linux
tags:
  - linux
abbrlink: d79b32e9
date: 2024-06-06 09:00:12
---
之前安装todesk没有搞定，总是连不上，于是又把它卸载了。卸载的时候把pulseaudio.x86_64也给卸载了。然后发现没有音量控制条了。然后又给安装回来
```
sudo dnf install pulseaudio
```
结果mplayer也出问题了。播放视频的时候卡住，其中一个问题是：
```
do_connect: could not connect to socket
```
于是在~/.mplayer/config中加入：
```
lirc=no
```
然后还是播放不了，出现问题：
```
MPlayer SVN-r38423-13 (C) 2000-2023 MPlayer Team

Playing let_it_go_original.mp4.
libavformat version 58.76.100 (external)
libavformat file format detected.
[mov,mp4,m4a,3gp,3g2,mj2 @ 0x7f6043a46660]Protocol name not provided, cannot determine if input is local or a network protocol, buffers and access patterns cannot be configured optimally without knowing the protocol
[lavf] stream 0: video (h264), -vid 0
[lavf] stream 1: audio (aac), -aid 0, -alang und
VIDEO:  [H264]  1280x720  24bpp  24.000 fps  1593.8 kbps (194.5 kbyte/s)
X11 error: BadMatch (invalid parameter attributes)
Failed to open VDPAU backend libvdpau_nvidia.so: cannot open shared object file: No such file or directory
[vdpau] Error when calling vdp_device_create_x11: 1

```
然后目前还没搞定。不知哪位大神能帮忙啊。

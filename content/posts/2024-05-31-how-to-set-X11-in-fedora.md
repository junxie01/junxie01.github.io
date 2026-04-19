---
title: Fedora下如何登陆X11桌面
categories:
  - Linux
tags:
  - linux
abbrlink: 1d2a45f5
date: 2024-05-31 20:25:18
---
&emsp;&emsp;安装了todesk以后进行远程控制时卡在“connecting to free server 100%”，然后不动。怎么办？
<!--less-->
&emsp;&emsp;目前还不知道怎么办，todesk官网说要用x11桌面，现在的fedora已经默认用Wayland了。如何开启X11呢？编辑文件/etc/gdm/custom.conf就好了：
```
WaylandEnable=false
DefaultSession=gnome-xorg.desktop
```
&emsp;&emsp;然后重新登陆就发现Settings->about显示Windowing System X11了。
&emsp;&emsp;不过靠不靠谱还不知道，还没有将remote station修改成X11。切换成X11以后bilibili视频似乎看不了了。连自己电脑中的mp4视频也播放不了。x11落后了？

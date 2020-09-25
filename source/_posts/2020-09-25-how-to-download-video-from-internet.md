---
title: how_to_download_video_from_internet
categories:
  - web
tags:
  - video
abbrlink: e17f06b7
date: 2020-09-25 16:20:54
---
&emsp;&emsp;很多时候在线看视频遇到喜欢的就像下载下来慢慢欣赏。那如何下载呢？
<!-- more -->
&emsp;&emsp;每次都需要到某度搜索。结果大量的广告，烦银。搞定了吧，下次又给忘了。今天就记录一下，免得下次又去找某度，碍眼。
&emsp;&emsp;估计以后某度会没得搞头吧，除了广告还充斥着各路货色。知乎里面回答那么多，那么详细，自然是用手投票啦。
&emsp;&emsp;说回正题，总算搜到一个强大的python程序，叫做you-get。说是下啥平台的视频都行。安装命令是这个样子的：
```
sudo pip3 install you-get
```
&emsp;&emsp;然后要下载视频的话就运行这个命令：
```
you-get 视频网址
```
&emsp;&emsp;就可以下载了。so easy。妈妈再也不用担心。。。慢着，下载下来是flv，虽然高清，但似乎一些视频软件打不开，编辑不能。咋办？转换格式呗。
&emsp;&emsp;哎～我又不争气的用了某度。果然，浪费我大把时间还弄得不快。什么在线转换，要么只能转小视频（极小），要么买app咯，气人。转换个格式，我买个app干嘛。这样子就可以了：
```
ffmpeg -i input.flv -c copy output.mp4
```
&emsp;&emsp;哈，大工告成。

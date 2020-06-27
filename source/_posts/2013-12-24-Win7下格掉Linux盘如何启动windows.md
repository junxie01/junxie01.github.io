---
title: Win7下格掉Linux盘如何启动windows
categories:
  - Linux
tags:
  - grub
abbrlink: 60954
date: 2013-12-24 01:40:27
---

&emsp;&emsp;在win7下用系统的磁盘管理工具把原来的fedora14给格了，然后重启就只能进入grub，试了安装盘修复也不行。

在grub中输入命令：

``` bash
grub>rootnoverify (hd0,0) 
grub>makeactive 
grub>chainloader +1
grub>boot
```

&emsp;&emsp;奏效。进入了windows。然后下载clear mbr （还原清新畅快的mbr，大概格掉了grub）。

然后大功告成。


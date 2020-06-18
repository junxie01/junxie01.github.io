---
title: 如何让Elementray OS取消自动更新检查
categories: Linux
tags:
  - Linux
abbrlink: 47982
date: 2020-06-18 10:24:18
---

&emsp;&emsp;我的HP笔记本上的Linux系统安装的是Elementary OS。这是个基于Ubuntu的注重界面美观的系统。是挺漂亮的，但几乎每天那个引用中心都会跳出来，帮我检查更新。
<!-- more -->
![应用中心](app.png)
&emsp;&emsp;这很烦人，尤其是还有出错，不能忍。所以必须让它停止自己更新啊。解决办法是这样。在文件/etc/apt/apt.conf.d/10periodic中将第一行的1改为0，成这样：
```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
```
0表示false，自然就不帮您自动更新了。

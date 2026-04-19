---
title: '运行LaTeX 遇到 ! LaTeX Error: File `xxx` not found.'
categories:
  - Linux
tags:
  - LaTeX
abbrlink: 6cb6ca71
date: 2024-06-06 10:26:10
---
运行LaTeX的时候遇到! LaTeX Error: File `xxx' not found.这个错误的时候该怎么办？
<!--less-->
这样就可以了
```
sudo dnf install 'tex(xxx)'
```
然后就会帮你安装缺失的文件。

---
title: 安装完fedora32之后
categories: '-- Linux'
tags: '-- 日记'
abbrlink: 186eae32
date: 2021-03-02 14:54:16
---
&emsp;&emsp;话说这台工作站已经有点“老了”，于是重新买了一台，美滋滋。5分钟安装了个fedora32，记录一下干了些啥。
<!-- more -->
## 换阿里源并更新
```bash
sudo mv /etc/yum.repos.d/fedora.repo /etc/yum.repos.d/fedora.repo.backup
sudo mv /etc/yum.repos.d/fedora-updates.repo /etc/yum.repos.d/fedora-updates.repo.backup
sudo wget -O /etc/yum.repos.d/fedora.repo http://mirrors.aliyun.com/repo/fedora.repo
sudo wget -O /etc/yum.repos.d/fedora-updates.repo http://mirrors.aliyun.com/repo/fedora-updates.repo
sudo yum makecache
sudo dnf update
```
## 给root设密码
```bash
sudo passwd root
```

## 改主机名
```
sudo hostnamectl set-hostname zbook7 --static
```

## 安装gmt6
```
dnf copr enable genericmappingtools/gmt
dnf install gmt
```

## 安装npm
在[这里](https://nodejs.org/en/download/)下载，然后安装。本来是想安装hexo，所以来安装这个软件。结果hexo一直搞不定。暂时就不理他了。

## 安装sac
在iris申请了一份sac102。源代码怎么都安装不成功，于是直接解压了可执行的二进制文件。

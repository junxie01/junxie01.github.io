---
title: 重新安装Elementary OS系统
abbrlink: b808b485
categories:
  - Linux
tags:
  - 日记
date: 2021-07-23 15:44:13
---
&emsp;&emsp;之前买的新电脑Zbook还行，安装了fedora 32（见{% post_link after-fedora32 %}）以后结果出现各种问题。包括，不能安装sac，rdseed，hexo，wikimedia。一气之下就安装回了Elementary OS。这里记录一下Elementary OS的配置。
<!-- more -->
## 软件更新管理器
安装命令如下：
```bash 
sudo apt update
sudo apt install software-properties-common software-properties-gtk
```
安装完以后在application里面输入app就可以运行了。挑选合适的镜像，然后更新系统。

## 中文输入法安装
安装命令如下：
```bash
sudo apt-get remove ibus   # 卸载ibus
sudo apt-get remove scim 
sudo apt-get autoremove   # 删除依赖包
sudo add-apt-repository ppa:fcitx-team/nightly
sudo apt-get update
sudo apt-get install im-switch fcitx fcitx-config-gtk fcitx-sunpinyin fcitx-module-cloudpinyin fcitx-googlepinyin   
sudo im-switch -s fcitx -z default
```

## 安装google-chrome浏览器
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install -f   # 自动安装依赖
```

## Hot corner快速显示桌面

```bash
sudo apt install wmctrl
wmctrl -k on
```
命令wmctrl -k on为显示桌面，将其放在System Settings/Desktop/Hot Corners/Custom Command就可以了。

## 安装hexo，SAC，rdseed，gmt一点问题都没有。

to be continued.

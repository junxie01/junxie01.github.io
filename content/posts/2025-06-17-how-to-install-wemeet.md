---
title: Fedora 40如何安装腾讯会议
tags:
  - Linux
categories:
  - Linux
abbrlink: 91c0c63d
date: 2025-06-17 13:20:08
---
&emsp;&emsp;没想到腾讯开发了Linux版本下的腾讯会议。
<!--less-->
&emsp;&emsp;那怎么安装呢？
&emsp;&emsp;我用了老办法，就是google咯，呃不是，我用的bing。搜索出来的第一条是知乎答案。于是按照说明开始安装了。首先在[腾讯主页](https://meeting.tencent.com/download)下载deb安装包。只有deb安装包，看样子还是ubuntu比较流行啊。
&emsp;&emsp;接下来按照说明安装alien。
```
sudo dnf install alien
```
&emsp;&emsp;alien可以将deb格式和rpm格式进行转换。还挺不错。转换命令是：
```
sudo alien -r deb包
```
&emsp;&emsp;然后就生成了一个rpm包，就可以安装了。。。吧。。。
&emsp;&emsp;不好意思，有依赖问题，怎么都搞不定。
&emsp;&emsp;事实上我犯了个错误啊，现在搜索引擎已经落伍了啊。我立马把问题输给了豆包啊。它说可以这么安装：
 * 安装Flatpak
```
sudo dnf install flatpak
```
嗯，我已经安装了。什么时候安装的呢。
 * 添加Flathub仓库：
```
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```
 * 按转腾讯会议：
```
flatpak install flathub com.tencent.wemeet
```
 * 运行
```
flatpak run com.tencent.wemeet
```

&emsp;&emsp;然后。。。安装速度慢的可以啊。我直接Ctrl+C掐了。
&emsp;&emsp;然后我在应用中心直接搜wemeet，就出现了WemeetApp，点击就安装了。好用的很。
&emsp;&emsp;Linux也变成了点击就运行的玩意儿了啊。

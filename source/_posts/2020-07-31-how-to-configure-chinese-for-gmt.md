---
title: 如何在elementaryOS下让gmt支持中文
categories:
  - gmt
tags:
  - 中文
abbrlink: 5bc68c30
date: 2020-07-31 23:03:04
---
&emsp;&emsp;有些时候用gmt画图需要添加一些中文标注。之前在fedora里用gmt4的时候配置过一次。现在用的是elementaryOS+gmt5.4.3怎么配置中文呢？
<!-- more -->
&emsp;&emsp;与centos啦fedora不一样,elementaryOS是基于ubuntu的。ghostscript中文配置文件不是在/usr/share/ghostscript/conf.d/cidfmap.zh_CN 而是在/etc/ghostscript/cidfmap.d/90gs-cjk-resource-gb1.conf[^1]。
&emsp;&emsp;也不用像fedora下面需要安装ghostscript-chinese-zh_CN，而elementaryOS的中文支持已经预装了。知道了中文配置文件的位置以后就十分方便。我们只需要把自己需要的字体下载下来就好了。例如需要windows字体的话就把\C:\Windows\Fonts下面的字体文件拷贝到/usr/share/fonts/winfonts下面。
&emsp;&emsp;下面就是老套路了。在中文配置文件末尾加上：
```
/STSong-Light << /FileType /TrueType /Path (/usr/share/fonts/winfonts/simsun.ttc) /SubfontId 0 /CSI [(GB1) 4] >> ;
/STFangsong-Light << /FileType /TrueType /Path (/usr/share/fonts/winfonts/simfang.ttf) /SubfontId 0 /CSI [(GB1) 4] >> ;
/STHeiti-Regular << /FileType /TrueType /Path (/usr/share/fonts/winfonts/simhei.ttf) /SubfontId 0 /CSI [(GB1) 4] >> ;
/STKaiti-Regular << /FileType /TrueType /Path (/usr/share/fonts/winfonts/simkai.ttf) /SubfontId 0 /CSI [(GB1) 4] >> ; 
```
&emsp;&emsp;然后更新字体map：
```
sudo update-gsfontmap
```
&emsp;&emsp;最后在gmt的字体配置文件/usr/share/gmt/postscriptlight/PSL_custom_fonts.txt加上：
```
STSong-Light--UniGB-UTF8-H 0.700 1
STFangsong-Light--UniGB-UTF8-H 0.700 1
STHeiti-Regular--UniGB-UTF8-H 0.700 1
STKaiti-Regular--UniGB-UTF8-H 0.700 1
```
&emsp;&emsp;用gmt pstext -L就可以看到添加的四中字体：
[gmt pstext -L显示的新添加4中字体](pstext.png)
&emsp;&emsp;然后就大功告成了。

[^1]:https://www.cnblogs.com/gisalameda/p/6840662.html

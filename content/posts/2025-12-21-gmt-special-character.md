---
title: gmt特殊字符
tags:
  - special character
categories:
  - gmt
abbrlink: a84a6285
date: 2025-12-21 20:28:34
---
&emsp;&emsp;每次想输入特殊字符例如上下标、乘除什么的都得去官方网站找，挺麻烦。
<!--less-->
最重要的是以下两个表：
{% asset_img a.png %}
至于是参考左边的Standard+还是右边的ISOLation1+，就要用命令
```
gmt get PS_CHAR_ENCODING
```
查看你的编码方式了。
另外如果了12号字体(Symbol)或34号字体(ZapfDingbats)则查下面这个表：
{% asset_img b.png %}
好了，搞定。自求多福哈，嘿嘿。

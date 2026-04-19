---
title: gmt的投影方式
tags:
  - gmt
categories:
  - gmt
abbrlink: '1247724'
date: 2025-11-23 15:24:13
---
&emsp;&emsp;每次画图都东找西找，多麻烦。别找了看这里就好了。
<!--less-->
&emsp;&emsp;其实参见[GMT文档](https://docs.generic-mapping-tools.org/6.0/cookbook/map_projections.html)就可以了。不过，一般我们画图不需要每个参数都知道吧。下面就列出几个典型的投影方式和例子，免得以后到处找。
## 蒙卡托投影
  首先是Mercator投影，最开始学的时候就是用这个。GMT主页说它可能是最著名的。它是等角圆柱形投影。

{% asset_img mercater.png 蒙卡托投影 %}

脚本如下：
```
#!/bin/bash
gmt begin mercater png
gmt coast -R90/140/10/50 -JM6i -Bxa10f5 -Bya10f5 -Dl -W0p -A5000 -Ggray
gmt end
```

## 米勒投影
  米勒投影把整个地球搞的挺方，比其他的扁的好看一点儿。

{% asset_img miller.png 米勒投影 %}

```
#!/bin/bash
gmt begin miller png
gmt coast -R-180/180/-90/90 -JJ6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 圆柱等积投影
  可以画矩形扁扁的地球。

{% asset_img cyl1.png "圆柱等积投影" "width:800,height:600" %}

```
#!/bin/bash
gmt begin cyl1 png
gmt coast -R-180/180/-90/90 -JY0/0/6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 圆柱等距投影
  也是扁扁的地球。

{% asset_img cyl2.png 圆柱等距投影 %}

```
#!/bin/bash
gmt begin cyl2 png
gmt coast -R-180/180/-90/90 -JQ6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 方位等距投影
  一般以某个点为中心的画法，例如接收函数台站和事件分布。

<img src="/gmt-projection/azi1.png" >


```
#!/bin/bash
gmt begin azi1 png
gmt coast -Rg -JE0/0/6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 正投影
  从无限远处看地球。可以简单理解为外星人视角。

<img src="/gmt-projection/orth.png" >

```
#!/bin/bash
gmt begin orth png
gmt coast -R-180/180/-90/90 -JG0/0/6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 透视投影
  gmt文档说是飞行器视角，我愿意称之为上帝视角，你想怎么看怎么看。

  -JG0/0/6000/90/0/0/60/60/5i 

  - 投影中心的经度和纬度（0ºE/0ºN）。
  - 观测者海拔高度（以公里为单位，6000 公里）。如果该值小于 10，则假定为观测者到地心的距离（以地球半径为单位）。如果附加“r”，则表示观测者到地心的距离（以公里为单位）。
  - 方位角以度为单位（90 度为正东）。相当于往东飞。
  - 倾斜角度（0度）。这是相对于天顶的视角，0度表示垂直向下看，60度倾斜角表示从地平线以上30度角看。
  - 旋转角度（0度）。这是图像的视轴旋转（顺时针方向）。180度旋转模拟倒飞的情况。
  - 视场的宽度和高度以度为单位（60）。这个数字取决于你是用肉眼观察（在这种情况下，你的视野大约为 60º 宽），还是用双筒望远镜等工具观察。

<img src="/gmt-projection/per.png" >

```
#!/bin/bash
gmt begin per png
gmt coast -R-180/180/-90/90 -JG0/0/6000/90/0/0/60/60/5i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 罗宾逊投影


<img src="/gmt-projection/rob.png" >

```
#!/bin/bash
gmt begin rob png
gmt coast -R-180/180/-90/90 -JN5i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 莫尔维德投影

<img src="/gmt-projection/moll.png">

```
#!/bin/bash
gmt begin moll png
gmt coast -Rd -JW5i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

## 埃克特投影
  好像很多全球成像结果就是用的这个投影。

<img src="/gmt-projection/eck.png" >
```
#!/bin/bash
gmt begin eck png
gmt coast -Rd -JKf5i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
```

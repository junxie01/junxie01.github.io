---
title: 鼠标点击位置记录
tags:
  - python
categories:
  - work
abbrlink: 1da3e56a
date: 2025-05-10 15:43:38
---
&emsp;&emsp;有些时候需要抓取别人图片中的点的信息，应该怎么整？

<!--less-->
&emsp;&emsp;当然是找作者要咯！不过有时可能没办法（例如可能联系不上作者/作者说找不到数据了/作者不想给你/作者说你自己提取吧）或则并不需要他图片中的点的准确信息的时候，我们可以自己去点。之前有个perl脚本，但找不到了（这又体现了整理资料和做笔记的必要性），现在python很方便的，调用pynput的Listener就好了。记录鼠标点击的脚本如下：
```
from pynput.mouse import Listener
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    filename="mouse_clicks.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

def on_click(x, y, button, pressed):
    if pressed:
        message = f"{x} {y}"
        print(message)  # 输出到屏幕
        logging.info(message)  # 写入日志文件
        if button == button.right:
            # 停止监听器
            return False

# 启动鼠标监听器
with Listener(on_click=on_click) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("监听器已被用户中断。")
```
&emsp;&emsp;这个脚本会记录鼠标左键的位置，输出到mouse_clicks.log文件中。mouse_clicks.log文件有三列:

2025-05-07T17:01:33 1977 1576

分别表示点击的时间，x和y坐标。其中y坐标是下面大上面小。此外点击鼠标右键或者输入Ctrl+C就可以结束记录。我一般是怎么做的呢？我先点击图片左下角得到（x0,y0），点击右下角得到(x1,y0)，点击左上角得到(x0,y1)，然后点击你想要的点。得到mouse_clicks.log以后就可以这么画图（gmt）。
```
dat=mouse_clicks.log
#获得x0,y0,x1,y1，他们是参考点
x0=`awk 'NR==1{print $2}' ${dat}`
y0=`awk 'NR==1{print $3}' ${dat}`
x1=`awk 'NR==2{print $2}' ${dat}`
y1=`awk 'NR==3{print $3}' ${dat}`
#获得横纵轴长度（屏幕尺度）
xs=`echo "$x1-$x0" |bc` 
ys=`echo "$y0-$y1" |bc`

awk -v x0=$x0 -v y0=$y0 -v xs=$xs -v ys=$ys 'NR>3{print ($2-x0)/xs*2000-1000,(y0-$3)/ys*1500}' ${dat} | gmt psxy -R -J -O -K -W3p,black >>$ps
#这里（2000，1500）是横纵轴实际尺度，-1000表示实际位置调整。
```
&emsp;&emsp;注意，这种方法仅仅适用于线性笛卡尔坐标，其他的各种投影都不行。
&emsp;&emsp;以后得加上这句：脚本/程序不保证正确性，自求多幅(no warranty/use at your own risk)。

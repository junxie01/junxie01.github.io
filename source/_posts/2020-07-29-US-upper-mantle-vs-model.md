---
title: 基于宽频带背景噪声面波的美国三维上地幔横波速度结构模型
categories:
  - work
tags:
  - model
abbrlink: 77d4f89d
date: 2020-07-29 02:30:10
---
![Maps of Vs structure in the upper mantle and major geological units modified from Fenneman (1917). The color bar labels are V S in km/s (top) and perturbation in percentage (bottom).](figure5.png)
<!-- less -->
&emsp;&emsp;利用宽频带的背景噪声面波做了美国三维上地幔横波速度结构，该工作做了x年。我不会告诉你这项工作做了多久，说出来都害sao。文章终于在2018年发表，文章链接在[这里](https://link.springer.com/article/10.1007/s00024-018-1881-2)，如果有需要可以找我要全文。
&emsp;&emsp;做模型真的是需要大量细致的工作。这篇文章的主要贡献是表明只用背景噪声面波也可以做的比较深，比较准，另外就是为community提供了一个新的模型。怎奈自己的地质背景太差，看不到啥突出的科学问题，还被审稿人批评说，‘你做的啥工作啊，像本科生的作业。’心塞。师兄说的对，应该多向可能对你的工作感兴趣的人请教，例如动力学方向的人啊之类的。
&emsp;&emsp;老板建议把这个模型挂在[IRIS EMC](https://ds.iris.edu/ds/products/emc-earthmodels/)里头，推广推广，让大伙儿都用用。我觉得不错，于是今天终于把它放到了IRIS里面。点击[这里](https://ds.iris.edu/ds/products/emc-us-upper-mantle-vsxiechuyang2018/)就可以看到我的模型了。里面有netcdf格式的数据可以下载。如果有需要可以找我要更细致的结果。
&emsp;&emsp;IRIS EMC需要的是netcdf格式的模型数据。IRIS有提供把txt文本格式的模型转换成netcdf的[python脚本](https://github.com/iris-edu/emc-tools)。另外向IRIS EMC提交模型的要求也可以这他们的[网页](https://ds.iris.edu/ds/products/emc-contributionguide/)看到，按照他们的要求把netcdf文件准备好，然后写一个说明文档一并发送给product@iris.washington.edu就完事了。
&emsp;&emsp;netcdf是2进制文件。要查看其头段信息的话可以用命令ncdump -h xxx.nc（安装netcdf-bin），要读取其参数信息可以用命令ncks（安装nco）。其实IRIS EMC也提供了将netcdf转换成txt文本的[python脚本](https://github.com/iris-edu/emc-tools)，非常方便。
&emsp;&emsp;求合作啊。我擅长处理数据，要是您能看到啥地学科学问题那真是求之不得啊。笑cry。

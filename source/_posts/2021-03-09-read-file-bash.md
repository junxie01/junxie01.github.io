---
title: bash里如何循环读取文件
categories:
  - Linux
tags:
  - Linux
abbrlink: e96b8da2
date: 2021-03-09 15:51:21
---
&emsp;&emsp;Bash操作简单，可以处理简单的计算等。有些时候会遇到文件的读取问题，那如何对文件进行循环逐行读取呢？
<!-- more -->
&emsp;&emsp;这样就可以了:
```bash
while read -r line
do
   array=(${line///})  
   echo ${array[1]}
done < the_file
```

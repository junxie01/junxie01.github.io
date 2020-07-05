---
title: hexo图片显示
categories: web
tags:
  - next
  - web
abbrlink: 25823
date: 2020-05-31 02:26:29
---
网站上没有图片是不行的，无图无真相。解决办法在[这里](https://blog.csdn.net/qq_38148394/article/details/79997971)，主要是利用了插件hexo-assrt-image。所以先安装这个插件：
``` bash
npm install hexo-asset-image --save
```
安装完以后将网站配置文件的post_assrt_folder字段的值改为true。每次在利用hexo new name 建新文章时，在source/_posts目录下会生成一个name的文件夹。把要调用的图放在该文件夹里，写文章的时候直接用该图的名字进行调用就行了。像这样：
```
![插图](a.png)
```
大功告成。

后来听来的说要让google搜到自己，博客的层级就不能太多。于是将
```
permalink: :year/:month/:day/:title/
```
改为了：
```
permalink: :title.html
```
结果图片怎么都显示不了。最后还得改回来。

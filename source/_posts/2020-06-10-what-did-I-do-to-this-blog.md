---
title: 我对这个博客做了什么
categories:
  - web
tags:
  - hexo
  - next
abbrlink: 58531
date: 2020-06-10 11:18:16
---

&emsp;&emsp;原本是想记笔记，写一些技术性的东西。然而现在为止好像还没有干啥正事。那我对这个博客做了些什么呢？干了这些：
<!-- more -->

## 重新下载了一次next主题
按{% post_link how-I-build-this-web 这个步骤 %}重新配置了一遍。之前不知道从哪里下载的一个山寨版还是啥的，应该是老版本，很多东西都没有。所以重新下载了最新版本。折腾了好久。对了，还干了好多无用功。网上搜来的很多教程版本都比较老。别马上按着别人的办法干，先看看主题的配置文件，或官方的文档。

## 插入脚注
请参见此神仙[^1]。 

## 隐藏网页底部 powered By Hexo
股沟出此大神[^2]的方法。
但事实上next已经集成了这个功能，直接在next/_config.yml里将powered改为false就可以了，像这样：
```
footer：
   xxx
   powered: false
   xxx
```

## 设置网站图标
同样来自这位大神[^2]。最重要的是找到自己喜欢的图片放在next/source/images里，然后在next/_config.yml里这样干就好了：
```
favicon:
  small: /images/j-icon-16x16.png
  medium: /images/j-icon-32x32.png
  apple_touch_icon: /images/icon.png
  safari_pinned_tab: /images/icon.png

```

## 设置标签云。
按照这位大仙[^3]的操作弄好了标签云，但是发现它不在正中啊。于是找到了tag cloud的[github](https://github.com/MikeCoder/hexo-tag-cloud)。里面有一句：
```
<canvas width="250" height="250" id="resCanvas" style="width:100%">
```
那个100%前面是一个冒号，而大仙[^3]写做等号。我发现等号就偏右边，冒号就在正中，很奇怪。

## 字数和阅读时长统计
请参见[^4]。

## 添加版权信息。
根据此大仙[^5]的说明弄好了以后，发现署名”前面的cc图标老是乱码（一个叉）。那怎么可以，弄了半天没弄好。结果人家next已经集成了。在next/_config.yml里面这样就好了。
```
creative_commons:
  license: by-nc-sa
  sidebar: true
  post: true
  language:
```

## 添加google广告到post里
参见[^6]。

## 加动态背景图片
根据这位大仙[^7]的方法弄的。
动态图片感觉太慢了。我在百度下了一个，有阳光森林，人，牛。感觉还不错，希望不要侵权。

## 侧边栏圆角
搜索到这位大神[^8]。我的Scheme选的是Pisces，所以先在next/source/css/_variables/Pisces.styl里面改一下变量
```
$border-radius                    = 5px;
```
然后到next/source/css/_schemes/Pisces/_layout.styl里面的.header-inner(对应菜单栏)字段改
```
border-radius: $border-radius;
```
在.content-wrap(对应文章页面)字段改
```
border-radius: $border-radius;
```
如此改完，然后......不对劲。在主页菜单栏和文章页面确实变圆角了，然而站点概况不是圆角。然而往下拖动，直到看不到菜单栏的时候，站点概况就变圆角了，不能忍。所以可能还要改siderbar字段。可惜_layout.styl里面木有。诶，我发现有next/source/css/_schemes/Pisces/_sidebar.styl文件。打开看。果然找到了。.sidebar字段是没有border-radius变量的，于是我添加了
```
border-radius: $border-radius;
```
除此以外，还看到了.sidebar-inner字段。也一并改了。这下就大功告成了。忘了说。这些字段的另一个变量是background，把它替换成
```
background: rgba(255,255,255,0.9);
```
就可以让博客变透明了。
## 运行时间
参见[^9]。
## 永久链接permalink
参见[^10]。首先安装程序：
```
npm install hexo-abbrlink --save
```
然后在_config.yml中设置：
```
permalink: posts/:abbrlink/
abbrlink:
  alg: crc32
  rep: hex
permalink_defaults:
pretty_urls:
  trailing_index: false # Set to false to remove trailing 'index.html' from permalinks
  trailing_html: false # Set to false to remove trailing '.html' from permalinks
```
大功搞成。

## 点击头像回到主页
设置请查看{% post_link avatar-to-homepage 这篇文章 %}

## 首页文章加框

设置请查看{% post_link frame %}

## 封面模式
参见[^11]。下载这个插件：
```
npm install --save hexo-less
```
然后作用与'<!--more-->'类似，但'<!--less-->'前面的部分不会显示到文章主题部分。

## 站内引用语法
这样:
```
{% post_link post_name %}
```
出来默认是博文题目，或者自己取个名字。
```
{% post_link post_name 点击查看%}
```


 [^1]:https://github.com/kchen0x/hexo-reference
 [^2]:https://blog.csdn.net/as480133937/article/details/100138838
 [^3]:https://blog.csdn.net/Aoman_Hao/article/details/89416634
 [^4]:https://github.com/theme-next/hexo-symbols-count-time
 [^5]:https://wylu.me/posts/e0424f3f/
 [^6]:https://juejin.im/post/5c95d230e51d45124e35cef6#comment
 [^7]:https://blog.diqigan.cn/posts/add-background-picture-for-next.html 
 [^8]:http://eternalzttz.com/hexo-next.html
 [^9]:https://www.93bok.com/Hexo网站运行时间添加/
[^10]:https://github.com/Rozbo/hexo-abbrlink
[^11]:https://github.com/fuchen/hexo-less

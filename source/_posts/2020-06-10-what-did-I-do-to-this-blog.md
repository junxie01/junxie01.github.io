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

1. 重新下载了一次next主题，重新配置了一遍。之前不知道从哪里下载的一个山寨版还是啥的，应该是老版本，很多东西都没有。所以重新下载了最新版本。折腾了好久。对了，还干了好多无用功。网上搜来的很多教程版本都比较老。别马上按着别人的办法干，先看看主题的配置文件，或官方的文档。

2. 插入脚注[^1]。 

3. 隐藏网页底部 powered By Hexo[^2]。但事实上next已经集成了这个功能，直接在next/_config.yml里将powered改为false就可以了，像这样：
```
footer：
   xxx
   powered: false
   xxx
```

4. 设置网站图标[^2]。最终要的是找到自己喜欢的图片放在next/source/images里，然后在next/_config.yml里这样干就好了：
```
favicon:
  small: /images/j-icon-16x16.png
  medium: /images/j-icon-32x32.png
  apple_touch_icon: /images/icon.png
  safari_pinned_tab: /images/icon.png

```

5. 设置标签云。按照这位大仙[^3]的操作弄好了标签云，但是发现它不在正中啊。于是找到了tag cloud的[github](https://github.com/MikeCoder/hexo-tag-cloud)。里面有一句：
```
<canvas width="250" height="250" id="resCanvas" style="width:100%">
```
那个100%前面是一个冒号，而大仙[^3]写做等号。我发现等号就偏右边，冒号就在正中，很奇怪。

6. 字数和阅读时长统计[^4]。

7. 添加版权信息。根据此大仙[^5]的说明弄好了以后，发现署名”前面的cc图标老是乱码（一个叉）。那怎么可以，弄了半天没弄好。结果人家next已经集成了。在next/_config.yml里面这样就好了。
```
creative_commons:
  license: by-nc-sa
  sidebar: true
  post: true
  language:
```

8. 添加google广告到post里[^6]。

9. 加动态背景图片[^7]。动态图片感觉太慢了。我在百度下了一个，有阳光森林，人，牛。感觉还不错，希望不要侵权。

10. 侧边栏圆角[^8]。

11. 运行时间[^9]。

[^1]:https://github.com/kchen0x/hexo-reference
[^2]:https://blog.csdn.net/as480133937/article/details/100138838
[^3]:https://blog.csdn.net/Aoman_Hao/article/details/89416634
[^4]:https://github.com/theme-next/hexo-symbols-count-time
[^5]:https://wylu.me/posts/e0424f3f/
[^6]:https://juejin.im/post/5c95d230e51d45124e35cef6#comment
[^7]:https://blog.diqigan.cn/posts/add-background-picture-for-next.html 
[^8]:http://eternalzttz.com/hexo-next.html
[^9]:https://www.93bok.com/Hexo网站运行时间添加/

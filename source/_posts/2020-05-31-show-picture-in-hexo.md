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
结果图片怎么都显示不了。果然permalink和post_assrt_folder是相互影响的。最后还得改回来。结果又不行了。将node_modules/hexo-asset-image/index.js替换一下[^1]然后才行。

当然我还是喜欢简洁一点的地址。我又将permalink改为了：
```
permalink: :title.html
```
如此，在运行
```
hexo g
```
的时候程序会将图片拷贝到public/name 下面。然而，引用的时候图片的地址会变为blogip/image.png自然就无法显示。
在node_modules/hexo-asset-image/index.js里可以看到这句话
```
  console.info&&console.info("update link as:-->"+config.root + link + src);
```
表明图片的地址是blogip+link+图片名称。所以这里是link出错了。
在link赋值的部分找到：
```
var beginPos = getPosition(link, '/', 3) + 1;
var endPos = link.lastIndexOf('/') + 1;
link = link.substring(beginPos, endPos);
```
之前的link是博客的位置。begionPos是'/'在link中第三次出现的位置下一位。这个定义是我需要的。endPos就不需要了。
所以改为：
```
link = link.substring(beginPos);
```
然后link后面没有'/'，就加一个：
```
link = link.concat("/");
```
然后图片位置就准备了。然后就大功告成。
[^1]:https://blog.csdn.net/xjm850552586/article/details/84101345

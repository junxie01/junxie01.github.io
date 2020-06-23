---
title: hexo next点击头像回到主页
categories: web
tags:
  - web
  - hexo
  - next
abbrlink: 26129
date: 2020-06-23 09:58:16
---

&emsp;&emsp;有了头像以后，看到头像一般就想点一点，点击了可以回到主页不是挺好的吗。
<!-- more -->
&emsp;&emsp;网上高手还是挺多。例如这位[上仙](http://eternalzttz.com/hexo-next.html)说要找到文件/themes/next/layout/_macro/sidebar.swig然后做修改。
```
+ <a href="/">
    <img class="site-author-image" itemprop="image"
       src="{{ url_for( theme.avatar.url | default(theme.images + '/avatar.gif') ) }}"
       alt="{{ author }}" />
+ </a>
```
&emsp;&emsp;于是我也这么干。但是，然而，怎么我的sidebar.swig没有这个avatar.gif的语句呢。瞎折腾也明白。后来试了一下：
```
find . -name sidebar*
```
&emsp;&emsp;然后找到了themes/next/layout/_partials/sidebar/site-overview.swig。在里面做修改
```
+ <a href="/">
<img class="site-author-image" itemprop="image" alt="{{ author }}"
src="{{ url_for(theme.avatar.url) }}">
+ </a>
```
Finally, it works.

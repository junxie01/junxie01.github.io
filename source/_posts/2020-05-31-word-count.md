---
title: next网站字数统计
categories: web
tags:
  - next
  - web
abbrlink: 22869
date: 2020-05-31 01:29:36
---
想给网站显示字数统计，搜到[这里](https://www.jianshu.com/p/baea8c95e39b)。根据说明开始设置。结果网站都差点挂掉。检查了好久也没有发现问题，以为玩完了。然后马上开始重新建hexo。结果还是有问题。后来终于发现在网站设置文件插入功能字段时误插到其他字段导致出错。注销以后问题就修复了。然后又搜索到[这里](https://blog.csdn.net/mqdxiaoxiao/article/details/93670772)。没想到搞定了，使用的插件是hexo-symbols-count-time。设置步骤如下：

<!-- more -->
## 1. 安装插件

``` bash
$ npm install hexo-symbols-count-time --save
```

## 2. 配置文件设置

在网站配置文件中加入如下字段：
```
symbols_count_time:
  symbols: true                # 文章字数统计
  time: true                   # 文章阅读时长
  total_symbols: true          # 站点总字数统计
  total_time: true             # 站点总阅读时长
  exclude_codeblock: false     # 排除代码字数统计
```

## 3. 主题配置文件设置

在主题配置文件加入如下字段：
```
# Post wordcount display settings
# Dependencies: https://github.com/theme-next/hexo-symbols-count-time
symbols_count_time:
  separated_meta: true     # 是否另起一行（true的话不和发表时间等同一行）
  item_text_post: true     # 首页文章统计数量前是否显示文字描述（本文字数、阅读时长）
  item_text_total: false   # 页面底部统计数量前是否显示文字描述（站点总字数、站点阅读时长）
  awl: 4                   # Average Word Length
  wpm: 275                 # Words Per Minute（每分钟阅读词数）
  suffix: mins
```

然后大功告成。


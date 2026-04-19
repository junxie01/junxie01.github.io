---
title: hexo插入图片
abbrlink: fb888a8a
date: 2025-11-23 20:19:43
categories: 
  - web
tags:
  - hexo
  - web
---
&emsp;&emsp;hexo显示图片显示有问题，怎么整？
<!--less-->
之前讲过怎么引用图片见{% post_link show-picture-in-hexo hexo图片显示 %}。但今天发现了奇怪的问题。那就是当我用gmt画图的时候，如果画出来的是球形图片时，这一句
```
{% asset_img picture_name %}
```
就不行了，显示不出来。然后就发现了这句：
```
<img src="/post_name/picture_name" >
```
这就可以了。不过这也不是办法，因为如果所有图片都存放在post_name目录下，那个人网站就太臃肿了。之前有个[网站](https://sm.ms/)，可以免费上传图片，然后分配一个网址给你，然后用这一句
```
![](picture_address)
```
然而这个网站在国内登陆出现问题了。于是问了Kimi，它列出了8个：
| 名称 | 网址 | 单张上限 | 有效期 | 外链速度 | 备注 |
|---|---|---|---|---|---|
| **Imgur** | https://imgur.com | 200 MB | 永久 | 全球 CDN | 免注册即可上传，直链秒开，Hexo 最常用 |
| **PostImage** | https://postimages.org | 10 MB | 永久 | 全球 CDN | 支持一键论坛/Markdown格式，复制即用 |
| **ImgBB** | https://imgbb.com | 32 MB | 永久 | 全球 CDN | 可匿名上传，提供HTML/Markdown直链 |
| **路过图床** | https://imgchr.com | 10 MB | 永久 | 国内 CDN | 中文界面，免登录，支持批量，国内访问飞快 |
| **Voooe图床** | https://voooe.cn | 25 MB | 永久 | 全球加速 | 拖放上传，自动生成Markdown代码 |
| **魔法师图床** | https://bgm.tv/img | 20 MB | 永久 | 国内节点 | 直连不跳转，适合博客插图 |
| **Telegraph-Image** | https://telegra.ph | 5 MB | 永久 | Cloudflare | 免注册，纯静态，上传即得直链 |
| **Imgbox** | https://imgbox.com | 10 MB | 永久 | 欧美节点 | 界面极简，可原图保存 |

看起来很不错。有空试试。

---
title: hexo如何给文章加框
categories:
  - web
tags:
  - hexo
  - web
abbrlink: 43f10f83
date: 2024-05-28 15:25:54
---
hexo next主题如何给文章加框？
<!-- less -->
找到hexo/themes/next/source/css/_common/components/post/index.styl
将：
```
  if (hexo-config('motion.transition.post_block')) {
    .post-block, .pagination, .comments {
      visibility: hidden;
    }
  }
```
改为：
```
  if (hexo-config('motion.transition.post_block')) {
   .post-block{
     visibility: hidden;
     margin-top: 60px;
     margin-bottom: 60px;
     padding: 25px;
     -webkit-box-shadow: 0 0 5px rgba(202, 203, 203, 1);
     -moz-box-shadow: 0 0 5px rgba(202, 203, 204, 1);
     }
   .pagination, .comments {
      visibility: hidden;
    }
```
